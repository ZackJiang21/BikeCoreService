import os

from flask import Flask

from core.model import db

PROJECT_DIR_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
SRC_DIR_ROOT = PROJECT_DIR_ROOT + "/core"

def create_app():
    app = Flask(__name__)
    # init alchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:shihang123@localhost:3306/bike_db?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
    db.app = app
    db.init_app(app)

    return app