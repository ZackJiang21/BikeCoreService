import logging
import os
import platform
import sys

import cv2
from flask import Flask
from flask_socketio import SocketIO, emit
from tqdm import tqdm

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)


@socketio.on('start_process')
def start_process(msg):
    print(msg)
    process_video()


def process_video():
    try:
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
                sys.path.append('../../python');
                # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
                # sys.path.append('/usr/local/python')
                from openpose import pyopenpose as op
        except ImportError as e:
            print(
                'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "../../../models/"

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        cap = cv2.VideoCapture("out.mp4")
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        for i in tqdm(range(int(frame_count))):
            ret, frame = cap.read()
            frame_count += 1
            if not ret:
                logger.error("frame %s read error", str(i))
                cap.release()
                break
            datum = op.Datum()
            datum.cvInputData = frame
            opWrapper.emplaceAndPop([datum])

            key_points = datum.poseKeypoints[0]
            emit('test', key_points.tolist())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    socketio.run(app)
