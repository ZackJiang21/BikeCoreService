import flask
from flask import jsonify, request

from core.model import db
from core.model.report import Report

report_blueprint = flask.Blueprint('report_blueprint', __name__)


@report_blueprint.route("/report", methods=['GET'])
def get_report_by_user():
    user_id = request.args.get('userId')
    reports = Report.query.filter(Report.user_id == user_id).all()
    report_list = [b.as_dict() for b in reports]
    return jsonify(report_list)


@report_blueprint.route("/report/<report_id>", methods=['DELETE'])
def delete_bike(report_id):
    Report.query.filter(Report.id == report_id).delete()
    db.session.commit()
    return report_id
