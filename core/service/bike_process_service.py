import base64
import os
import platform
import sys
import time
import uuid

import cv2
import numpy as np
from flask_socketio import emit

from core.config.app_config import logger
from core.lib import HKIPcamera1
from core.lib import HKIPcamera2
from core.lib import HKIPcamera3
from core.model import db
from core.model.report import Report
from core.model.report_detail import ReportDetail
from core.util.angle_calculator import AngleCalculator
from core.util.report_img_util import get_img_path
from core.util.util import mod_with_none

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH'] = os.environ[
                                 'PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
        import pyopenpose as op
    else:

        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('/home/zhangjiang/code/openpose/openpose/build/python');  #
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "/home/zhangjiang/code/openpose/openpose/models/"

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e


class BikeService(object):
    LEFT_INDEX = (0, 5, 6, 7, 12, 13, 14, 19)
    RIGHT_INDEX = (0, 2, 3, 4, 9, 10, 11, 22)
    FRONT_INDEX = (0, 2, 3, 4, 9, 10, 11, 22, 5, 6, 7, 12, 13, 14, 19, 1, 8)

    def __init__(self, socketio):
        self._is_canceled = False
        self.socketio = socketio
        name = str('admin')  # 管理员用户名
        pw = str('shihang123')  # 管理员密码
        HKIPcamera1.init('10.90.90.91', name, pw)  # front
        HKIPcamera2.init('10.90.90.92', name, pw)  # left
        HKIPcamera3.init('10.90.90.93', name, pw)  # right

        self.__rotate_input_before_pose_estimation = True
        self.__emit_image_shrink_ratio_times_of_two = 2  # should be times of 2
        self.__emit_image_shrink_ratio = 2 ** self.__emit_image_shrink_ratio_times_of_two  # should be times of 2

        self.sleep_time = 0.001
        # after emit, must sleep

    def process_video(self, user, bike):
        try:
            self._is_canceled = False
            self._is_really_canceled = False

            datum = op.Datum()

            frame1_tmp = HKIPcamera1.getframe()
            frame2_tmp = HKIPcamera2.getframe()
            frame3_tmp = HKIPcamera3.getframe()

            # we need images of same size to concatnate, if not, will give error
            assert frame1_tmp.cols == frame2_tmp.cols == frame3_tmp.cols
            assert frame1_tmp.rows == frame2_tmp.rows == frame3_tmp.rows

            angle_calculator = AngleCalculator(width=frame1_tmp.cols, height=frame1_tmp.rows)

            while True:
                if self._is_really_canceled:
                    if angle_calculator.knee_path_pic is not None:
                        cv2.imwrite("final_knee_path.png", angle_calculator.knee_path_pic)
                    self.__save_report(user, bike, angle_calculator)
                    break

                if self._is_canceled:
                    self._is_really_canceled = True

                frames_np_rotate, key_points_front, key_points_left, key_points_right = self.get_key_point(datum)

                # calculate angles
                angle_calculator.update_every_frame(key_points_front, key_points_right, key_points_left,
                                                    is_last_frame=self._is_really_canceled)

                self.socketio.sleep(self.sleep_time)

                r = angle_calculator.knee_path_pic_crop_ratio
                wid, hei, channel = angle_calculator.frame_shape
                small_wid = int(wid // r)
                small_hei = int(hei // r)
                small_knee_path_pic = angle_calculator.knee_path_pic[
                                      0 + (wid - small_wid) // 2: -(wid - small_wid) // 2,
                                      0 + (hei - small_hei) // 2: -(hei - small_hei) // 2, :]

                self._emit_image(*frames_np_rotate, small_knee_path_pic)

                emit('points', {"front": [(mod_with_none(point[0], self.__emit_image_shrink_ratio),
                                           mod_with_none(point[1], self.__emit_image_shrink_ratio),
                                           point[2])
                                          for point in key_points_front],
                                "left": [(mod_with_none(point[0], self.__emit_image_shrink_ratio),
                                          mod_with_none(point[1], self.__emit_image_shrink_ratio),
                                          point[2])
                                         for point in key_points_left],
                                "right": [(mod_with_none(point[0], self.__emit_image_shrink_ratio),
                                           mod_with_none(point[1], self.__emit_image_shrink_ratio),
                                           point[2])
                                          for point in key_points_right],
                                "angles": angle_calculator.report_angles,
                                "distance": angle_calculator.report_distance},
                     ignore_queue=True)


        except Exception as e:
            logger(e)

    def get_key_point(self, datum):
        frames_np_rotate = []
        # frame1_np front
        for i in range(1, 4):  # [1, 2, 3]
            frame_np = np.array(eval('HKIPcamera{}'.format(i)).getframe())

            # rotate camera to fit human size
            frame_np_rotate = cv2.rotate(frame_np, cv2.ROTATE_90_COUNTERCLOCKWISE)

            frames_np_rotate.append(frame_np_rotate)

            self.single_width = frame_np_rotate.shape[1]
        process_frame = np.concatenate(frames_np_rotate, axis=1)
        datum.cvInputData = process_frame
        opWrapper.emplaceAndPop([datum])
        key_points_front, key_points_left, key_points_right = [(None, None, None)] * 25, [(None, None, None)] * 25, [
            (None, None, None)] * 25
        if datum.poseKeypoints.shape:

            for poseKeypoints in datum.poseKeypoints:

                key_points = poseKeypoints.tolist()

                x_max = max([point[0] for point in key_points])

                if 0 <= x_max and x_max < self.single_width and not self._filter_keypoint(self.FRONT_INDEX, key_points):
                    key_points_front = [(None, None, None) if point[:2] == [0.0, 0.0] else tuple(point) for point in
                                        key_points]
                elif self.single_width <= x_max and x_max < self.single_width * 2 and not self._filter_keypoint(
                        self.LEFT_INDEX, key_points):
                    key_points_left = [(None, None, None) if point[:2] == [0.0, 0.0] else (
                        point[0] - self.single_width, point[1], point[2]) for point in key_points]
                elif not self._filter_keypoint(self.RIGHT_INDEX, key_points):
                    key_points_right = [(None, None, None) if point[:2] == [0.0, 0.0] else (
                        point[0] - 2 * self.single_width, point[1], point[2]) for point in key_points]
        return frames_np_rotate, key_points_front, key_points_left, key_points_right

    def cancel_process_video(self):
        logger.info("canceling process.")
        self._is_canceled = True

    def __save_report(self, user, bike, angle_calculator):
        try:
            file_name = user['name'] + ' ' + str(int(round(time.time() * 1000)))
            knee_path_img = str(uuid.uuid1())
            knee_path_dir = get_img_path(knee_path_img)
            report = Report(user_id=user['id'],
                            name=file_name)
            db.session.add(report)
            db.session.flush()
            cv2.imwrite(knee_path_dir, angle_calculator.knee_path_pic)
            report_detail = ReportDetail(report_id=report.id,
                                         model=bike['model'],
                                         size=bike['size'],
                                         year=bike['year'],
                                         type=bike['type'],
                                         angles=angle_calculator.report_angles,
                                         distances=angle_calculator.report_distance,
                                         knee_path_img=knee_path_img
                                         )
            db.session.add(report_detail)
            db.session.commit()
        except Exception as er:
            logger.error('report roll back %s' % er)
            db.session.rollback()

    def _emit_image(self, frame_front, frame_left, frame_right, frame_knee_path):

        for _ in range(self.__emit_image_shrink_ratio_times_of_two):
            frame_front = cv2.pyrDown(frame_front)
            frame_left = cv2.pyrDown(frame_left)
            frame_right = cv2.pyrDown(frame_right)
            # frame_knee_path = cv2.pyrDown(frame_knee_path)
        cv2.rectangle(frame_front, (50, 120), (130, 280), (0, 0, 255), 1)
        cv2.rectangle(frame_right, (5, 140), (175, 240), (0, 0, 255), 1)
        cv2.rectangle(frame_left, (5, 140), (175, 240), (0, 0, 255), 1)
        img_bytes_front = cv2.imencode('.jpeg', frame_front)[1].tostring()
        img_bytes_left = cv2.imencode('.jpeg', frame_left)[1].tostring()
        img_bytes_right = cv2.imencode('.jpeg', frame_right)[1].tostring()
        img_bytes_knee_path = cv2.imencode('.jpeg', frame_knee_path)[1].tostring()

        emit('image', {
            'img_right': self._get_base64_encode_str(img_bytes_right),
            'img_left': self._get_base64_encode_str(img_bytes_left),
            'img_front': self._get_base64_encode_str(img_bytes_front),
            'img_knee_path': self._get_base64_encode_str(img_bytes_knee_path)}, ignore_queue=True)

    def _get_base64_encode_str(self, input):
        encode_bytes = base64.b64encode(input)
        return str(encode_bytes, 'utf-8')

    def _filter_keypoint(self, indexList, keypoints):
        score = 0
        for index in indexList:
            score += keypoints[index][2]
        if score / len(indexList) < 0.4:
            return True
        return False
