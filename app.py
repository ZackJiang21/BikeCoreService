from flask import Flask
from flask_socketio import SocketIO

from core.service.bike_process_service import bike_service
from core.config.app_config import logger

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('start_process')
def start_process(msg):
    logger.info(msg)
    bike_service.process_video()


@socketio.on('cancel_process')
def cancel_process():
    bike_service.cancel_process_video()


if __name__ == '__main__':
    socketio.run(app)
