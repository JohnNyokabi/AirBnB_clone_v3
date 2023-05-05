#!/usr/bin/python3
"""Script for State view"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Retrieves a list of state objects"""

    state_objs = storage.all(State)

    states = [obj.to_dict() for obj in state_objs.values()]
    if request.method == 'GET':
        return jsonify(states)
    elif request.method == 'POST':
        my_dict = request.get_json()

        if my_dict is None:
            abort(400, 'Not a JSON')
        if my_dict.get("name") is None:
            abort(400, 'Missing name')
        new_state = State(**my_dict)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def state_id(state_id):
    """updates the states object"""
    if request.method == 'GET':
        for state in states:
            if state.get('id') == state_id:
                return jsonify(state)
        abort(404)
    elif request.method == 'PUT':
        my_dict = request.get_json()

        if my_dict is None:
            abort(400, 'Not a JSON')
        for state in state_objs.values():
            if state.id == state_id:
                state.name = my_dict.get("name")
                state.save()
                return jsonify(state.to_dict()), 200
        abort(404)

    elif request.method == 'DELETE':
        for obj in state_objs.values():
            if obj.id == state_id:
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200
        abort(404)
