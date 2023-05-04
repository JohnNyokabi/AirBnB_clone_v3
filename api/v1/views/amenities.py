#!/usr/bin/python3
"""AirBnB clone Amenity view"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def all_amenities():
    """Defines GET and POST methods for amenities route"""
    amenities = storage.all("Amenity").values()
    if request.method == 'GET':
        return jsonify([amenities.to_dict()], amenities=amenities)

    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    if res.get("name") is None:
        abort(400, "Missing name")
    amenity = Amenity(**res)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_id(amenity_id):
    """Defines the update methods for Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    avoid = {"id", "created_at", "updated_at"}
    [setattr(amenity, k, v) for k, v in res.items() if k not in avoid]
    amenity.save()
    return jsonify(amenity.to_dict())
