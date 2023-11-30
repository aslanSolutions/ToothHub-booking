from venv import logger
from flask import Blueprint, jsonify, request
from apifairy import body, response
from .schema import WishlistSchema
from.db import users
from bson import ObjectId 
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity


bp = Blueprint('Wishlist', __name__, url_prefix='/wishlist')
wishlist_collection = users['Wishlist']

@bp.route('/create', methods=['POST'])
@jwt_required()
def register_wishlist():
    # Create wishlist
    payload = request.get_json()
    logger.debug(f"Received payload: {payload}")

    # Instantiate the schema and validate the payload
    schema = WishlistSchema()
    errors = schema.validate(payload)
    if errors:
        return jsonify({"message": "Validation error", "errors": errors}), 400

    # Extract the JWT identity from the request
    current_user_identity = get_jwt_identity()

    # Make a validation request to the authentication service
    validate_url = "http://127.0.0.1:5000/auth/validate"
    headers = {"Authorization": request.headers.get('Authorization')}
    validate_response = requests.get(validate_url, headers=headers)

    if validate_response.status_code == 200:
        # User is valid, proceed with wishlist creation
        result = wishlist_collection.insert_one(payload)
        new_wishlist_id = result.inserted_id
        created_wishlist = wishlist_collection.find_one({'_id': new_wishlist_id})

        # Convert ObjectId to string before returning the response
        created_wishlist['_id'] = str(created_wishlist['_id'])
        return jsonify(created_wishlist), 201
    else:
        # Validation failed
        return jsonify({"message": "User validation failed"}), validate_response.status_code



@bp.route('/<int:wishlist_id>', methods=['GET'])
@response(WishlistSchema, 200)
def get_wishliat(wishlist_id):
    # Retrieve a dentist by ID
    wishlist = users.find_one({'_id': wishlist_id})

    if wishlist:
        return wishlist
    else:
        return jsonify({"message": f"No wishlist found with ID {wishlist_id}"}), 404


@bp.route('/', methods=['GET'])
@response(WishlistSchema, 200)
def get_all_wishlists():
    # Retrieve all dentsit list
    all_patinets = list(wishlist_collection.find({}))
    return all_patinets


@bp.route('/<int:wishlist_id>', methods=['PATCH'])
@response(WishlistSchema, 200)
@body(WishlistSchema, 200)
def update_wishlist(wishlist_id):
    # Update a wishlist by ID
    existing_wishlist = users.find_one({'_id': wishlist_id})

    if not existing_wishlist:
        return jsonify({"message": f"No wishlist found with ID {wishlist_id}"}), 404

    # Get the updated data from the request payload
    updated_data = request.get_json()

    # Validate the updated data against the schema
    errors = WishlistSchema.validate(updated_data)
    if errors:
        return jsonify({"message": "Validation error", "errors": errors}), 400

    # Update the existing patinet with the new data
    users.update_one({'_id': wishlist_id}, {'$set': updated_data})

    # Return the updated wishlist
    updated_wishlist = users.find_one({'_id': wishlist_id})
    return updated_wishlist

@bp.route('/<int:wishlist_id>', methods=['DELETE'])
def delete_wishlist(wishlist_id):
    # Delete a wishlist account by ID
    result = users.delete_one({'_id': wishlist_id})

    if result.deleted_count == 1:
        return jsonify({"message": f"wishlist with ID {wishlist_id} deleted successfully"}), 200
    else:
        return jsonify({"message": f"No dentist found with ID {wishlist_id}"}), 404

@bp.route('/delete_all', methods=['DELETE'])
def delete_all_wishlists():
    # Delete all patinets from the collection
    result = wishlist_collection.delete_many({})
    return jsonify({"message": f"{result.deleted_count} wishlist deleted"}), 200

