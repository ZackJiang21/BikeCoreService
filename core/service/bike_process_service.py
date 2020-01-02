import os
import platform
import sys
import base64
import time

import cv2
import numpy as np
from flask_socketio import emit

from core.config.app_config import logger
from core.lib import HKIPcamera1
from core.lib import HKIPcamera2
from core.lib import HKIPcamera3

from core.util.angle_calculator import AngleCalculator
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
        sys.path.append('/home/zhangjiang/code/openpose/openpose/build/python'); #
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
    def __init__(self, socketio):
        self._is_canceled = False
        self.socketio = socketio
        name = str('admin')  # 管理员用户名
        pw = str('shihang123')  # 管理员密码
        HKIPcamera1.init('10.90.90.91', name, pw) #front
        HKIPcamera2.init('10.90.90.92', name, pw) #left
        HKIPcamera3.init('10.90.90.93', name, pw) #right

        self.__rotate_input_before_pose_estimation = True
        self.__emit_image_shrink_ratio_times_of_two = 2 # should be times of 2
        self.__emit_image_shrink_ratio = 2 ** self.__emit_image_shrink_ratio_times_of_two # should be times of 2

        self.sleep_time = 0.001
        # after emit, must sleep

    def process_video(self):
        try:
            self._is_canceled = False

            angle_calculator = AngleCalculator()

            datum = op.Datum()

            frame1_tmp = HKIPcamera1.getframe()
            frame2_tmp = HKIPcamera2.getframe()
            frame3_tmp = HKIPcamera3.getframe()

            # we need images of same size to concatnate, if not, will give error
            assert frame1_tmp.cols == frame2_tmp.cols == frame3_tmp.cols
            assert frame1_tmp.rows == frame2_tmp.rows == frame3_tmp.rows

            while True:
                t0 = time.time()
                if self._is_canceled:
                    break

                frames_np_rotate = []
                # frame1_np front
                for i in range(1, 4): #[1, 2, 3]
                    frame_np = np.array(eval('HKIPcamera{}'.format(i)).getframe())

                    # rotate camera to fit human size
                    frame_np_rotate = cv2.rotate(frame_np, cv2.ROTATE_90_COUNTERCLOCKWISE)

                    frames_np_rotate.append(frame_np_rotate)

                    self.single_width = frame_np_rotate.shape[1]

                process_frame = np.concatenate(frames_np_rotate, axis=1)

                datum.cvInputData = process_frame

                t1 = time.time()

                opWrapper.emplaceAndPop([datum])

                t2 = time.time()

                key_points1, key_points2, key_points3 = [(None, None, None)] * 25, [(None, None, None)] * 25, [(None, None, None)] * 25

                if datum.poseKeypoints.shape:

                    for poseKeypoints in datum.poseKeypoints:

                        key_points = poseKeypoints.tolist()

                        x_max = max([point[0] for point in key_points])

                        if 0 <= x_max and x_max < self.single_width:
                            key_points1 = [(None, None, None) if point[:2] == [0.0, 0.0] else tuple(point) for point in key_points]
                        elif self.single_width <= x_max and x_max < self.single_width * 2:
                            key_points2 = [(None, None, None) if point[:2] == [0.0, 0.0] else (point[0] - self.single_width, point[1], point[2]) for point in key_points]
                        else:
                            key_points3 = [(None, None, None) if point[:2] == [0.0, 0.0] else (point[0] - 2 * self.single_width, point[1], point[2]) for point in key_points]

                # calculate angles
                angle_calculator.update_every_frame(key_points1, key_points3, key_points2)

                self.socketio.sleep(self.sleep_time)

                t3 = time.time()

                self._emit_image(*frames_np_rotate)

                emit('points', {"front": [(mod_with_none(point[0], self.__emit_image_shrink_ratio),
                                           mod_with_none(point[1], self.__emit_image_shrink_ratio),
                                           point[2])
                                          for point in key_points1],
                                "left": [(mod_with_none(point[0], self.__emit_image_shrink_ratio),
                                           mod_with_none(point[1], self.__emit_image_shrink_ratio),
                                           point[2])
                                          for point in key_points2],
                                "right": [(mod_with_none(point[0], self.__emit_image_shrink_ratio),
                                           mod_with_none(point[1], self.__emit_image_shrink_ratio),
                                           point[2])
                                          for point in key_points3],
                                "angles": angle_calculator.report_angles,
                                "distance": angle_calculator.report_distance},
                                ignore_queue=True)

                t4 = time.time()

                logger.debug('real fps {}, detection {}, emit {}, sleep {}'.format(round(1 / (t4 - t0), 1), t2 - t1, t4- t3, self.sleep_time))


        except Exception as e:
            logger(e)

    def cancel_process_video(self):
        logger.info("canceling process.")
        self._is_canceled = True


    def _emit_image(self, frame_front, frame_left, frame_right):

        for _ in range(self.__emit_image_shrink_ratio_times_of_two):
            frame_front = cv2.pyrDown(frame_front)
            frame_left = cv2.pyrDown(frame_left)
            frame_right = cv2.pyrDown(frame_right)

        img_bytes_front = cv2.imencode('.jpeg', frame_front)[1].tostring()
        img_bytes_left = cv2.imencode('.jpeg', frame_left)[1].tostring()
        img_bytes_right = cv2.imencode('.jpeg', frame_right)[1].tostring()

        emit('image', {
            'img_right': self._get_base64_encode_str(img_bytes_right),
            'img_left': self._get_base64_encode_str(img_bytes_left),
            'img_front': self._get_base64_encode_str(img_bytes_front)}, ignore_queue=True)


    def _get_base64_encode_str(self, input):
        encode_bytes = base64.b64encode(input)
        return str(encode_bytes, 'utf-8')


