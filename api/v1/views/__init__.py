#!/usr/bin/python3
'''
'''


from flask import Blueprint, jsonify
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
app_views = Blueprint('/api/v1', __name__)

index.init()
states.init_states()
cities.init_cities()
amenities.init_amenities()
users.init_users()
places.init_places()
places_reviews.init_places_reviews()
