#!/usr/bin/python3
"""Create new view for Place Reviews objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews(place_id):
    """retrieves list of all Review objects of place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([rev.to_dict() for rev in place.reviews])

    if request.method == 'POST':
        res = request.get_json()
        if res is None:
            abort(400, "Not a JSON")
        user_id = res.get("user_id")
        if user_id is None:
            abort(400, "Missing user_id")
        res["place_id"] = place_id
        if storage.get(User, user_id) is None:
            abort(404)
        if res.get("text") is None:
            abort(400, "Missing text")
        review = Review(**res)
        review.place_id = place_id
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def review_id(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        res = request.get_json()
        if res is None:
            abort(400, "Not a JSON")
        avoid = {"id", "user_id", "place_id", "created_at", "updated_at"}
        [setattr(review, k, v) for k, v in res.items() if k not in avoid]
        storage.save()
        return jsonify(review.to_dict()), 200
