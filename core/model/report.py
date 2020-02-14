from core.model import db
from core.model.user import User
from datetime import datetime
from sqlalchemy.sql import func


class Report(db.Model):
    __tablename__ = 't_report'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    create_time = db.Column(db.TIMESTAMP, default=func.now(), nullable=False)
    user = db.relationship(User, backref='report')

    def as_dict(self):
        report_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in report_dict.items():
            if key == 'create_time':
                report_dict['create_time'] = int(datetime.timestamp(value))
        return report_dict
