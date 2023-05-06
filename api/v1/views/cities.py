#!/usr/bin/python3
"""AirBnb City view"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities_by_state(state_id):
    """Defines GET and POST methods for cities object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        res = request.get_json()
        if res is None:
            abort(400, "Not a JSON")
        if res.get("name") is None:
            abort(400, "Missing name")
        new_city = City(**res)
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city_id(city_id):
    """Defines update methods for specific city ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        res = request.get_json()
        if res is None:
            abort(400, "Not a JSON")
        avoid = {"id", "state_id", "created_at", "updated_at"}
        [setattr(city, k, v) for k, v in res.items() if k not in avoid]
        storage.save()
        return jsonify(city.to_dict())
