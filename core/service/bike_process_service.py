import os
import platform
import sys
import base64

import cv2
import numpy as np
from flask_socketio import emit

from core.config.app_config import logger
from core.lib import HKIPcamera1
from core.lib import HKIPcamera2
from core.lib import HKIPcamera3

from core.util.angle_calculator import AngleCalculator

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

    def process_video(self):
        try:
            self._is_canceled = False

            # Custom Params (refer to include/openpose/flags.hpp for more parameters)
            params = dict()
            params["model_folder"] = "../../../models/"

            # Starting OpenPose
            opWrapper = op.WrapperPython()
            opWrapper.configure(params)
            opWrapper.start()

            angle_calculator = AngleCalculator()

            idx = 0
            while True:
                # time1 = time.time()
                if self._is_canceled:
                    break

                datum = op.Datum()

                # frame1 front
                frame = HKIPcamera1.getframe()
                # rotate camera to fit human size
                process_frame1 = cv2.pyrDown(np.rot90(np.array(frame)))
                datum.cvInputData = process_frame1
                opWrapper.emplaceAndPop([datum])
                if datum.poseKeypoints.shape:
                    key_points1 = datum.poseKeypoints[0].tolist()
                    # key_points should be list of tuples
                    # replace (0.0, 0.0) to (None, None)
                    key_points1 = [(None, None, None) if point[:2] == [0.0, 0.0] else tuple(point) for point in key_points1]

                else:
                    key_points1 = [(None, None, None)] * 25
                    logger.warn("can not detect person in camera 1")



                # frame2 left
                frame2 = HKIPcamera2.getframe()
                # rotate camera to fit human size
                process_frame2 = cv2.pyrDown(np.rot90(np.array(frame2)))
                datum.cvInputData = process_frame2
                opWrapper.emplaceAndPop([datum])
                if datum.poseKeypoints.shape:
                    key_points2 = datum.poseKeypoints[0].tolist()
                    key_points2 = [(None, None, None) if point[:2] == [0.0, 0.0] else tuple(point) for point in key_points2]

                else:
                    key_points2 = [(None, None, None)] * 25
                    logger.warn("can not detect person in camera 2")


                # frame3 right
                frame3 = HKIPcamera3.getframe()
                # rotate camera to fit human size
                process_frame3 = cv2.pyrDown(np.rot90(np.array(frame3)))
                datum.cvInputData = process_frame3
                opWrapper.emplaceAndPop([datum])
                if datum.poseKeypoints.shape:
                    key_points3 = datum.poseKeypoints[0].tolist()
                    key_points3 = [(None, None, None) if point[:2] == [0.0, 0.0] else tuple(point) for point in key_points3]
                else:
                    key_points3 = [(None, None, None)] * 25
                    logger.warn("can not detect person in camera 3")

                # emit frame3 no matter how
                self._emit_image(process_frame1, process_frame2, process_frame3)

                # calculate angles
                angle_calculator.update_every_frame(key_points1, key_points3, key_points2)
                emit('points', {"front": key_points1,
                                "left": key_points2,
                                "right": key_points3,
                                "angles": angle_calculator.report_angles,
                                "distance": angle_calculator.report_distance},
                                ignore_queue=True)
                # after emit, must sleep
                self.socketio.sleep(0.005)


        except Exception as e:
            logger(e)

    def cancel_process_video(self):
        logger.info("canceling process.")
        self._is_canceled = True


    def _emit_image(self, frame_front, frame_left, frame_right):
        img_bytes_front = cv2.imencode('.jpeg', frame_front)[1].tostring()
        img_bytes_left = cv2.imencode('.jpeg', frame_left)[1].tostring()
        img_bytes_right = cv2.imencode('.jpeg', frame_right)[1].tostring()
        emit('image', {
            'img_right': self._get_base64_encode_str(img_bytes_right),
            'img_left': self._get_base64_encode_str(img_bytes_left),
            'img_front': self._get_base64_encode_str(img_bytes_front) }, ignore_queue=True)


    def _get_base64_encode_str(self, input):
        encode_bytes = base64.b64encode(input)
        return str(encode_bytes, 'utf-8')


