#!/usr/bin/python3
"""  Cities RestFul API """

from flask import Blueprint, jsonify, abort, request
from models import storage
from models.city import City

import json


def init_cities():
    from api.v1.views import app_views

    @app_views.route('/states/<state_id>/cities', methods=['GET'])
    def get_all_cities_in_state(state_id=None):
        """ Get all cities in a state"""
        if id is not None and storage.get("State", id) is not None:
            cities = []
            for city in storage.all("City").values():
                if city.state_id == str(state_id):
                    cities.append(city.to_dict())
            return jsonify(cities)
        else:
            abort(404)

    @app_views.route('/cities/<city_id>', methods=['GET'])
    def get_city(city_id):
        """ Get City """
        city = storage.get("City", str(city_id))
        if city is not None:
            return jsonify(city.to_dict())
        abort(404)
