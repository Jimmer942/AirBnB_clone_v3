#!/usr/bin/python3
'''
'''


from flask import Blueprint, jsonify
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.places import *
app_views = Blueprint('/api/v1', __name__)

index.init()
states.init_states()
cities.init_cities()
places.init_places()
