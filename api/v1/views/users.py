#!/usr/bin/python3
"""  Users RestFul API """

from flask import jsonify, abort, request
from models import storage
from models.user import User


def init_users():
    from api.v1.views import app_views

    @app_views.route('/users', methods=['GET'], strict_slashes=False)
    def get_all_users():
        """ Get all users"""
        users = []
        for user in storage.all("User").values():
            users.append(user.to_dict())
        return jsonify(users)

    @app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
    def get_user(user_id):
        """ Get user """
        user = storage.get("User", str(user_id))
        if users is not None:
            return jsonify(user.to_dict())
        abort(404)

    @app_views.route('/users/<user_id>', methods=['DELETE'],
                     strict_slashes=False)
    def delete_user(user_id):
        """ Delete user """
        if user_id is not None:
            if storage.get("User", str(user_id)) is not None:
                storage.delete(storage.get("User", str(user_id)))
            else:
                abort(404)
        return jsonify({}), 200

    @app_views.route('/users', methods=['POST'],
                     strict_slashes=False)
    def create_user():
        """ Create user """
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        if 'email' not in request.json:
            return jsonify({"error": "Missing email"}), 400
        if 'password' not in request.json:
            return jsonify({"error": "Missing password"}), 400
        user = User(**request.get_json())
        storage.new(user)
        return jsonify(storage.get("User", user.id).to_dict()), 201

    @app_views.route('/users/<user_id>', methods=['PUT'],
                     strict_slashes=False)
    def update_user(user_id):
        """ Update user """
        if storage.get("User", str(user_id)) is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a Json"}), 400
        user = storage.get("User", str(user_id))
        for key, value in request.json.items():
            if (
                    key == 'id' or
                    key == 'email' or
                    key == 'created_at' or
                    key is not 'updated_at'
            ):
                pass
            else:
                setattr(user, key, value)
        user.save()
        return jsonify(storage.get("User", user.user_id).to_dict()), 200
