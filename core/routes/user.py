import flask
from flask import jsonify, request, abort
from core.model.user import User
from core.model import db

user_blueprint = flask.Blueprint('user_blueprint', __name__)


@user_blueprint.route("/user", methods=['GET'])
def get_all_user():
    user_list = User.query.all()
    user_dict_list = [u.as_dict() for u in user_list]
    return jsonify(user_dict_list)


@user_blueprint.route("/user", methods=['POST'])
def add_user():
    if not request.json or not request.json.get('name'):
        abort(400)
    user = User(name=request.json.get('name'),
                gender=request.json.get('gender'),
                age=request.json.get('age'),
                phone=request.json.get('phone'),
                email=request.json.get('email'))
    db.session.add(user)
    db.session.commit()
    return str(user.id)


@user_blueprint.route("/user/<userId>", methods=['DELETE'])
def delete_user(userId):
    User.query.filter(User.id == userId).delete()
    db.session.commit()
    return userId
