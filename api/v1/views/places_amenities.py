#!/usr/bin/python3
"""HTTP methods for API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """GET method for reviews"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """GET method for reviews within a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """DELETE method for reviews"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """PUT method for updating a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """POST method for creating a review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    required_fields = ['user_id', 'text']
    for field in required_fields:
        if field not in request.json:
            return jsonify({"error": f"Missing {field}"}), 400

    user_id = request.json['user_id']
    if storage.get(User, user_id) is None:
        abort(404)

    request.json['place_id'] = place_id
    review = Review(**request.json)
    review.save()
    return jsonify(review.to_dict()), 201
