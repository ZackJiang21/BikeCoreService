import os

import flask
from flask import jsonify, request, send_file, make_response, abort

from core.model import db
from core.model.report import Report
from core.model.report_detail import ReportDetail
from core.service.report_service import ReportService

report_blueprint = flask.Blueprint('report_blueprint', __name__)
report_service = ReportService()


@report_blueprint.route("/report", methods=['GET'])
def get_report_by_user():
    user_id = request.args.get('userId')
    reports = Report.query.filter(Report.user_id == user_id).all()
    report_list = [b.as_dict() for b in reports]
    return jsonify(report_list)


@report_blueprint.route("/report/<report_id>", methods=['PUT'])
def send_report_to_email(report_id):
    report_detail = ReportDetail.query.filter(ReportDetail.report_id == report_id).first()
    if report_detail is None:
        abort(404)
    report_service.send_to_email(report_detail)
    return str(report_id)


@report_blueprint.route("/report/<report_id>", methods=['GET'])
def get_report_by_id(report_id):
    report_detail = ReportDetail.query.filter(ReportDetail.report_id == report_id).first()
    if report_detail is None:
        abort(404)
    pdf_path = report_service.get_report_file(report_detail)
    rep = make_response(send_file(pdf_path))
    file_name = os.path.basename(pdf_path)
    rep.headers['Content-Disposition'] = "filename={}".format(file_name)
    return rep


@report_blueprint.route("/report/<report_id>", methods=['DELETE'])
def delete_bike(report_id):
    Report.query.filter(Report.id == report_id).delete()
    db.session.commit()
    return report_id
