#!/usr/bin/python3
"""  place RestFul API """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.place import Place
import json


def init_places():
    from api.v1.views import app_views

    @app_views.route(
                    '/cities/<id>/places',
                    methods=['GET'], strict_slashes=False)
    def get_places_by_citie(id=None):
        """ Get places by city """
        city = storage.get("City", id)
        if city is None:
            abort(404)
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)

    @app_views.route('/places/<id>', methods=['GET'], strict_slashes=False)
    def get_place(id=None):
        '''get place by id'''
        place = storage.get("Place", id)
        if place is None:
            abort(404)
        return jsonify(place.to_dict())

    @app_views.route('/places/<id>', methods=['DELETE'], strict_slashes=False)
    def delete_place(id=None):
        '''delete a place by id'''
        place = storage.get("Place", id)
        if place is None:
            abort(404)
        storage.delete(place)
        return jsonify({}), 200

    @app_views.route(
                    '/cities/<id>/places',
                    methods=['POST'], strict_slashes=False)
    def create_place_by_city(id=None):
        '''create a place'''
        city = storage.get("City", id)
        if city is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400
        if 'user_id' not in request.json:
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get("User", request.json['user_id'])
        if user is None:
            abort(404)
        if 'name' not in request.json:
            return jsonify({"error": "Missing name"}), 400
        place = Place(**request.json)
        place.city_id = id
        storage.new(place)
        return jsonify(storage.get("Place", place.id).to_dict()), 201

    @app_views.route('/places/<id>', methods=['PUT'], strict_slashes=False)
    def update_place(id=None):
        '''update a place'''
        place = storage.get("Place", id)
        if place is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400

        for key, value in request.json.items():
            if (
                key == 'id' or key == 'user_id' or
                key == 'city_id'
            ):
                pass
            else:
                setattr(place, key, value)
        storage.save()
        return jsonify(storage.get("Place", place.id).to_dict()), 200
