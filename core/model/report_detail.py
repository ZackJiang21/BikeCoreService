from core.model import db
from core.model.report import Report
import json


class Json(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


class ReportDetail(db.Model):
    __tablename__ = 't_report_ext'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey(Report.id, ondelete='CASCADE'), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    size = db.Column(db.String(16), nullable=False)
    year = db.Column(db.SmallInteger, nullable=False)
    type = db.Column(db.String(16), nullable=False)
    angles = db.Column(Json(), nullable=False)
    distances = db.Column(Json(), nullable=False)
    knee_path_img = db.Column(db.String(64), nullable=False)
    report = db.relationship(Report, backref='report_detail', uselist=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}