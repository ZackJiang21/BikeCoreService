# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform

from core.lib import HKIPcamera1
from core.lib import HKIPcamera2
from core.lib import HKIPcamera3
import numpy as np

from core.util.angle_calculator_bak import AngleCalculator

from core.config.app_config import logger

name = 'admin'  # 管理员用户名
pw = 'shihang123' # 管理员密码
HKIPcamera1.init('10.90.90.91', name, pw)  # front
HKIPcamera2.init('10.90.90.92', name, pw)  # left
HKIPcamera3.init('10.90.90.93', name, pw)  # right

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

# Flags

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../../models/"

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

angle_calculator = AngleCalculator()


while True:
    datum = op.Datum()

    # frame1 front
    frame = HKIPcamera1.getframe()
    process_frame1 = cv2.pyrDown(np.rot90(np.array(frame)))
    datum.cvInputData = process_frame1
    opWrapper.emplaceAndPop([datum])
    if datum.poseKeypoints.shape:
        key_points1 = datum.poseKeypoints[0].tolist()
        key_points1 = [(None, None, None) if point[:2] == [0.0, 0.0] else tuple(point) for point in key_points1]
    else:
        key_points1 = [(None, None, None)] * 25
        logger.warn("can not detect person in camera 1")

    # frame2 left
    frame2 = HKIPcamera2.getframe()
    process_frame2 = cv2.pyrDown(np.array(frame2))
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
    process_frame3 = cv2.pyrDown(np.array(frame3))
    datum.cvInputData = process_frame3
    opWrapper.emplaceAndPop([datum])
    if datum.poseKeypoints.shape:
        key_points3 = datum.poseKeypoints[0].tolist()
        key_points3 = [(None, None, None) if point[:2] == [0.0, 0.0] else tuple(point) for point in key_points3]
    else:
        key_points3 = [(None, None, None)] * 25
        logger.warn("can not detect person in camera 3")


    # calculate angles
    angle_calculator.update_every_frame(key_points1, key_points3, key_points2)
    a = 1

