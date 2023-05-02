#!/usr/bin/python3
"""Script for State view"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def all_states():
    """Defines GET and POST methods for route"""
    states = storage.all("State").values()
    if request.method == 'GET':
        return jsonify([states.to_dict()], states=states)

    res = request.get_json(silent=True)
    if (!res):
        return "Not a JSON", 400
    if res.get("name") is None:
        return "Missing name", 400
    state = State(**res)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>' methods=['GET', 'PUT', 'DELETE'])
def state_id(state_id):
    """updates the states object"""
    state = storage.get("State", state_id)
    if (!state):
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200

    res = request.get_json(silent=True)
    if (!new_dict):
        return "Not JSON", 400
    avoid = {"id", "created_at", "updated_at"}
    [setattr(state, k, v) for k, v in res.items() if k not in avoid]
    state.save()
    return jsonify(state.to_dict())
