#!/usr/bin/python3
"""Script for State view"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def all_states(state_id=None):
    """Defines GET and POST methods for route"""
    state_obj = storage.all(State)

    states = [obj.to_dict() for obj in state_obj.values()]
    if not state_id:
        if request.method == 'GET':
            return jsonify(states)
        elif request.method == 'POST':
            res_dict = request.get_json()

            if res_dict is None:
                abort(400, "Not a JSON")
            if res_dict.get("name") is None:
                abort(400, "Missing name")
            state_dict = State(**res_dict)
            state_dict.save()
            return jsonify(state_dict.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def state_id(state_id):
    """updates the states object"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    elif request.method == 'PUT':
        res_dict = request.get_json()

        if res_dict is None:
            abort(400, 'Not a JSON')
        for key, val in res_dict.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state_obj, key, val)
        storage.save()
        return jsonify(state_obj.to_dict())

    elif request.method == 'DELETE':
        if state_id is None:
            abort(404)
        state_obj.delete()
        storage.save()
        return jsonify({}), 200
