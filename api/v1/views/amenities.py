#!/usr/bin/python3
"""  Cities RestFul API """

from flask import Blueprint, jsonify, abort, request
from models import storage
from models.amenity import Amenity

import json


def init_amenities():
    from api.v1.views import app_views

    @app_views.route('/amenities', methods=['GET'], strict_slashes=False)
    def get_all_Amenities():
        """ Get all Amenities"""
        amenities = []
        for amenity in storage.all("Amenity").values():
            amenities.append(amenity.to_dict())
        return jsonify(amenities)

    @app_views.route('/amenities/<amenity_id>', methods=['GET'],
                     strict_slashes=False)
    def get_amenity(amenity_id):
        """ Get amenity """
        amenity = storage.get("Amenity", str(amenity_id))
        if amenity is not None:
            return jsonify(city.to_dict())
        abort(404)

    @app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                     strict_slashes=False)
    def delete_amenity(amenity_id):
        """ Delete amenity """
        if amenity_id is not None:
            if storage.get("Amenity", str(amenity_id)) is not None:
                storage.delete(storage.get("Amenity", str(amenity_id)))
            else:
                abort(404)
        return jsonify({}), 200

    @app_views.route('/amenities', methods=['POST'], strict_slashes=False)
    def create_amenity():
        """ Create states """
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400
        if 'name' not in request.json:
            return jsonify({"error": "Missing name"}), 400
        amenity = Amenity(**request.get_json())
        storage.new(amenity)
        return jsonify(storage.get("Amenity", amenity.id).to_dict()), 201

    @app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                     strict_slashes=False)
    def update_amenities(amenity_id):
        """ Update amenities """
        if storage.get("Amenity", str(amenity_id)) is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400
        amenity = storage.get("Amenity", str(amenity_id))
        for key, value in request.json.items():
            if (key == 'id' and key == 'created_at' and key == 'updated_at'):
                pass
            else:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(storage.get("Amenity", city.city_id).to_dict()), 200
