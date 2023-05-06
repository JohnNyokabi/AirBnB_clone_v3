#!/usr/bin/python3
"""Create a new view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places(city_id):
    """defines place object using GET and POST methods"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([plc.to_dict() for plc in city.places])

    if request == 'POST':
        res = request.get_json()
        if res is None:
            abort(400, "Not a JSON")
        user_id = res.get("user_id")
        if user_id is None:
            abort(400, "Missing user_id")
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if res.get("name") is None:
            abort(400, "Missing name")
        place = Place(**res)
        place.city_id = city_id
        place.save()
        return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place_id(place_id):
    """Updates the place ID objects with GET, PUT and DELETE methods"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        res = request.get_json()
        if res is None:
            abort(400, "Not a JSON")
        avoid = {"id", "user_id", "city_id", "created_at", "updated_at"}
        [setattr(place, k, v) for k, v in res.items() if k not in avoid]
        storage.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all place objects from JSON"""
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")

    states_id = res.get("states", [])
    cities_id = res.get("cities", [])
    amenities_id = res.get("amenities", [])
    places = []
    if states_id == cities_id == []:
        places = storage.all(Place).values()
    else:
        states = [
            storage.get(State, s_id) for s_id in states_id
            if storage.get(State, s_id)
        ]
        cities = [
            city for state in states for city in state.cities
        ]
        cities += [
            storage.get(City, c_id) for c_id in cities_id
            if storage.get(City, c_id)
        ]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]

    amenities = [
        storage.get(Amenity, a_id) for a_id in amenities_id
        if storage.get(Amenity, a_id)
    ]

    body = []
    for place in places:
        body.append(place.to_dict())
        for amenity in amenities:
            if amenity not in place.amenities:
                body.pop()
                break

    return jsonify(body)
