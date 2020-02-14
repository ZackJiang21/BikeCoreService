from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)
    from core.model.user import User
    from core.model.bike import Bike
    from core.model.report import Report
    from core.model.report_detail import ReportDetail
