from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app():
    from core.model.user import User
    from core.model.bike import Bike

