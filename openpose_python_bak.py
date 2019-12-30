# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse

from core.lib import HKIPcamera
import numpy as np


ip = str('10.90.90.91')  #摄像头IP地址，要和本机IP在同一局域网
name = str('admin')       #管理员用户名
pw = str('shihang123')      #管理员密码
HKIPcamera.init(ip, name, pw)
try:
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

    while True:
        frame = HKIPcamera.getframe()
        process_frame = cv2.pyrDown(np.array(frame))
        datum = op.Datum()
        datum.cvInputData = process_frame
        opWrapper.emplaceAndPop([datum])
        key_points = datum.poseKeypoints
        if datum.poseKeypoints.shape:
            key_points = datum.poseKeypoints[0]
except Exception as e:
    print(e)
    sys.exit(-1)
