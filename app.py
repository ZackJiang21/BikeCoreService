import os
print(os.__file__)
from flask_socketio import SocketIO

from core.service.bike_process_service import BikeService
from core.config.app_config import logger

from core import create_app
from core.model import db
import core.model as model
import core.routes as routes

import eventlet
eventlet.monkey_patch()

app = create_app()
model.init_app(app)
routes.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

bike_service = BikeService(socketio)

@socketio.on('start_process')
def start_process(msg):
    logger.info(msg)
    bike_service.process_video()


@socketio.on('cancel_process')
def cancel_process(rider_info):
    logger.info(rider_info)
    bike = rider_info['bike']
    user = rider_info['user']
    bike_service.cancel_process_video(user, bike)


if __name__ == '__main__':
    db.create_all()
    socketio.run(app, host="0.0.0.0", port=5000)
