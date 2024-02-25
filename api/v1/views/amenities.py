#!/usr/bin/python3
"""Amenities RestFul API"""

from flask import Blueprint, jsonify, abort, request
from models import storage
from models.amenity import Amenity

def init_amenities():
    """Initialize Amenities API endpoints"""

    amenities_bp = Blueprint('amenities_api', __name__)

    @amenities_bp.route('/amenities', methods=['GET'], strict_slashes=False)
    def get_all_amenities():
        """Get all amenities"""
        amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
        return jsonify(amenities)

    @amenities_bp.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
    def get_amenity(amenity_id):
        """Get amenity by ID"""
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())

    @amenities_bp.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
    def delete_amenity(amenity_id):
        """Delete amenity by ID"""
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    @amenities_bp.route('/amenities', methods=['POST'], strict_slashes=False)
    def create_amenity():
        """Create a new amenity"""
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in request.json:
            return jsonify({"error": "Missing name"}), 400
        amenity = Amenity(**request.json)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    @amenities_bp.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
    def update_amenity(amenity_id):
        """Update amenity by ID"""
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in request.json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200

    return amenities_bp
