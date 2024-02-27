# api/v1/views/index.py

from flask import jsonify
from api.v1.views import app_views  # Remove this line

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
