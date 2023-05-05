#!/usr/bin/python3
"""Create a new view for the User object"""
from api.v1.views import app_views
from models.user import User
from flask import request, abort, jsonify
from models import storage


@app_views.route('/users',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_users():
    """Defines list of all users with the POST and GET methods"""
    users = storage.all("User").values()
    if request.method == 'GET':
        return jsonify([users.to_dict()], users=users)

    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    if res.get("email") is None:
        abort(400, "Missing email")
    if res.get("password") is None:
        abort(400, "Missing password")

    user = User(**res)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def user_id(user_id):
    """defines specific user ID using GET, PUT and DELETE methods"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    avoid = {"id", "email", "created_at", "updated_at"}
    [setattr(user, k, v) for k, v in res.items() if k not in avoid]
    user.save()
    return jsonify(user.to_dict())
