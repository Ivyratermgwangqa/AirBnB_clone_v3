#!/usr/bin/python
""" holds class Place"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place

@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Searches for places based on JSON in the request body"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])

    places = []
    if not states and not cities and not amenities:
        places = storage.all("Place").values()
    else:
        if states:
            for state_id in states:
                state = storage.get("State", state_id)
                if state:
                    places.extend(state.cities)

        if cities:
            for city_id in cities:
                city = storage.get("City", city_id)
                if city:
                    places.append(city)

        if amenities:
            amenity_objs = [storage.get("Amenity", a_id) for a_id in amenities]
            for place in storage.all("Place").values():
                if all(amenity in place.amenities for amenity in amenity_objs):
                    places.append(place)

    result = [place.to_dict() for place in set(places)]  # Remove duplicates
    return jsonify(result)
