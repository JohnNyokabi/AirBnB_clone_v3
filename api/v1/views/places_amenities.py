#!/usr/bin/python3
"""Creates new view for places amenities objects"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.amenity import Amenity
from models.place import Place
import os


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def place_amenities(place_id):
    """Retrieves list of all Amenity objects"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        return jsonify([a.to_dict() for a in place.amenities])
    else:
        res = storage.get(Amenity, p_id) for p_id in place.amenity_ids
        return jsonify([res.to_dict()])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def update_place_amenities(place_id, amenity_id):
    """Updates Amenity object to a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if request.method == 'POST':
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict())
            else:
                place.amenities.append(amenity)
        else:
            if amenity.id in place.amenity_id:
                return jsonify(amenity.to_dict())
            else:
                place.amenity_id.append(amenity.id)

        storage.save()
        return jsonify(amenity.to_dict()), 201

    if request.method == 'DELETE':
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity not in place.amenities:
                abort(404)
        else:
            if amenity.id not in place.amenity_id:
                abort(404)
        amenity.delete()
        storage.save()
        return jsonify({}), 200
