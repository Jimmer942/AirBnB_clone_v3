#!/usr/bin/python3
"""  place RestFul API """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.state import State
import json


def init_places():
    from api.v1.views import app_views

    @app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
    def get_places_by_citie(city_id):
        """ Get places by city """
        city = storage.get("City", city_id)
        if city is None:
            abort(404)
        return jsonify(city.places)

    @app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
    def get_place(place_id):
        '''get place by id'''
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        return jsonify(place.to_dict())

    @app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
    def delete_place(place_id):
        '''delete a place by id'''
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        storage.delete(place)
        return jsonify({}), 200

    @app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
    def create_place_by_city(city_id):
        city = storage.get("City", city_id)
        if city is None:
            abort(404)
        if not request.json:
            return 'Not a JSON', 400
        if 'user_id' not in request.json:
            return 'Missing user_id', 400
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        if 'name' not in request.json:
            return 'Missing name', 400
        place = Place(**request.json)
        storage.new(place)
        return jsonify(storage.get("Place", place.id).to_dict()), 201

    @app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
    def update_place(place_id):
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        if not request.json:
            return 'Not a JSON', 400
        
        for key, value in request.json.items():
            setattr(place, key, value)
            storage.save()
        return jsonify(storage.get("Place", place.id).to_dict()), 200
