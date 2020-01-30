#!/usr/bin/python3
"""  Cities RestFul API """

from flask import Blueprint, jsonify, abort, request
from models import storage
from models.city import City

import json


def init_cities():
    from api.v1.views import app_views

    @app_views.route('/states/<state_id>/cities', methods=['GET'])
    def get_all_cities_in_state(state_id):
        """ Get all cities in a state"""
        if state_id is None:
            abort(404)
        if storage.get("State", str(state_id)) is not None:
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

    @app_views.route('/cities/<city_id>', methods=['DELETE'])
    def delete_city(city_id):
        """ Delete city """
        if city_id is not None:
            if storage.get("City", str(city_id)) is not None:
                storage.delete(storage.get("City", str(city_id)))
            else:
                abort(404)
        return jsonify({}), 200

    @app_views.route('/states/<state_id>/cities', methods=['POST'])
    def create_new_city(state_id):
        """ Create new city """
        if storage.get("State", str(state_id)) is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400
        if 'name' not in request.json:
            return jsonify({"error": "Missing name"}), 400
        r = request.get_json()
        r['state_id'] = str(state_id)
        city = City(**r)
        city.save()
        return jsonify(city.to_dict()), 201

    @app_views.route('/cities/<city_id>', methods=['PUT'])
    def update_city(city_id):
        """ Update city """
        if storage.get("City", str(city_id)) is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400
        city = storage.get("City", str(city_id))
        for key, value in request.json.items():
            setattr(city, key, value)
        storage.save()
        return jsonify(storage.get("City", city.city_id).to_dict()), 200
