#!/usr/bin/python3
"""Create a new view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places(city_id):
    """defines place object using GET and POST methods"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([plc.to_dict() for plc in city.places])

    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    user_id = res.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if res.get("name") is None:
        abort(400, "Missing name")
    res["city_id"] = city_id
    place = Place(**res)
    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def place_id(place_id):
    """Updates the place ID objects with GET, PUT and DELETE methods"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    avoid = {"id", "user_id", "city_id", "created_at", "updated_at"}
    [setattr(place, k, v) for k, v in res.items() if k not in avoid]
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Retrieves all place objects from JSON"""
    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    if len(res) == 0 or all(len(l) == 0 for l in data.values()):
        return jsonify([p.to_dict() for p in storage.all("Place").values()])

    places = []

    states = res.get("states")
    if states is not None and len(states) != 0:
        for s in states:
            state = storage.get("State", s)
            if state is not None:
                [[places.append(p) for p in c.places] for c in state.cities]

    cities = res.get("cities")
    if cities is not None and len(cities) != 0:
        for c in cities:
            city = storage.get("City", c)
            if city is not None:
                [places.append(p) for p in city.places]

    amenities = res.get("amenities")
    place_amenities = []
    if amenities is not None and len(amenities) != 0:
        for p in storage.all("Place").values():
            if type(storage) == DBStorage:
                amenity_ids = [a.id for a in p.amenities]
            else:
                amenity_ids = p.amenity_ids
            if set(amenities).issubset(set(amenity_ids)):
                p.__dict__.pop("amenities", None)
                p.__dict__.pop("amenity_ids", None)
                place_amenities.append(p)
        if len(places) != 0:
            places = list(set(places) & set(place_amenities))
        else:
            places = place_amenities

    return jsonify([p.to_dict() for p in places])
