#!/usr/bin/python3
""" API endpoints for status and statistics"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Statistics about the data"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
