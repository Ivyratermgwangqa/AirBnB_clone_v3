#!/usr/bin/python3
"""module views"""
from flask import Blueprint
from api.v1.views.index import index
from api.v1.views.states import states
from api.v1.views.cities import cities
from api.v1.views.places import places
from api.v1.views.places_reviews import reviews
from api.v1.views.places_amenities import amenities
from api.v1.views.users import users
from api.v1.views.amenities import amenities

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')
app_views.register_blueprint(index)
app_views.register_blueprint(states)
app_views.register_blueprint(cities)
app_views.register_blueprint(places)
app_views.register_blueprint(reviews)
app_views.register_blueprint(amenities)
app_views.register_blueprint(users)
