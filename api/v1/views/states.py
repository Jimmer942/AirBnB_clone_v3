#!/usr/bin/python3
"""  State RestFul API """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.state import State
import json


def init_states():
    from api.v1.views import app_views

    @app_views.route('/states', strict_slashes=False)
    @app_views.route('/states/<id>',  methods=['GET'], strict_slashes=False)
    def get_states(id=None):
        """ Get states """
        if id is not None:
            if storage.get("State", id) is not None:
                return jsonify(storage.get("State", id).to_dict())
            else:
                abort(404)
        states = []
        for state in storage.all("State").values():
            states.append(state.to_dict())
        return jsonify(states)

    @app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
    def delete_state(id=None):
        """ Delete states """
        if id is not None:
            if storage.get("State", id) is not None:
                storage.delete(storage.get("State", id))
            else:
                abort(404)
        return jsonify({}), 200

    @app_views.route('/states/', methods=['POST'], strict_slashes=False)
    def create_state():
        """ Create states """
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400
        if 'name' not in request.json:
            return jsonify({"error": "Missing name"}), 400
        state = State(**request.get_json())
        storage.new(state)
        return jsonify(storage.get("State", state.id).to_dict()), 201

    @app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
    def update_state(id):
        """ Update states """
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400
        if type(request.json) is not dict:
            return jsonify({"error": "Missing name"}), 400
        if storage.get("State", id) is not None:
            state = storage.get("State", id)
            for key, value in request.json.items():
                setattr(state, key, value)
            storage.save()
        else:
            abort(404)
        return jsonify(storage.get("State", state.id).to_dict()), 201
