#!/usr/bin/python3
"""HTTP methods for RESTFul API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_place(city_id=None):
    """GET places within cities"""
    list_places = []
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    else:
        all_places = storage.all("Place").values()
        for place in all_places:
            if place.city_id == str(city_id):
                list_places.append(place.to_dict())
        return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_places(place_id=None):
    """GET place method"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE', 'PUT'])
def place_methods(place_id=None):
    """DELETE and PUT methods"""
    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    if request.method == 'DELETE':
        obj_place.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        do_put = request.get_json()
        for k, v in do_put.items():
            if k != "id" and k != "created_at" and k != "updated_at" and k != "user_id" and k != "city_id":
                setattr(obj_place, k, v)
        obj_place.save()
        return jsonify(obj_place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_post(city_id):
    """POST method"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    user_id = request.json['user_id']
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    new_place = Place(**request.json)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201
