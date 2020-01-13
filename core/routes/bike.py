import flask
from core.model.bike import Bike
from flask import request, jsonify, abort
from core.model import db

bike_blueprint = flask.Blueprint('bike_blueprint', __name__)


@bike_blueprint.route("/bike", methods=['GET'])
def get_bikes_by_user():
    user_id = request.args.get('userId')
    bike_list = Bike.query.filter(Bike.user_id == user_id).all()
    bike_dict_list = [b.as_dict() for b in bike_list]
    return jsonify(bike_dict_list)


@bike_blueprint.route("/bike", methods=['POST'])
def add_bike():
    if not request.json:
        abort(400)
    user_id = request.args.get('userId')
    bike = Bike(model=request.json.get('model'),
                size=request.json.get('size'),
                year=request.json.get('year'),
                type=request.json.get('type'),
                user_id=user_id)
    db.session.add(bike)
    db.session.commit()
    return str(bike.id)


@bike_blueprint.route("/bike/<bikeId>", methods=['DELETE'])
def delete_bike(bikeId):
    Bike.query.filter(Bike.id == bikeId).delete()
    db.session.commit()
    return bikeId
