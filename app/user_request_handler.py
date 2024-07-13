import logging
from .logging_config import setup_logging
from config import get_config
import os
from flask import Flask, Blueprint, request, jsonify
from enum import Enum
from .validators import (
    validate_json,
    validate_email,
    validate_string_length,
    validate_numeric,
    validate_timestamp_id,
    validate_address,
)
from .firestore_helper import (
    add_document_to_collection,
    retrieve_document_from_collection,
)

bp = Blueprint("main", __name__)
config = get_config()
# Run setup_logging to configure logging
setup_logging()
# Create a logger
logger = logging.getLogger(__name__)


# Ensure the service account path is set
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise ValueError(
        "SERVICE_ACCOUNT_PATH environment variable is not set. Please provide the path to the service account JSON file."
    )

# Import Firebase Admin SDK and initialize it
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(cred)


@bp.route("/user/status", methods=["GET"])
def status_check():
    """
    Endpoint to check if the Flask application is running.
    Returns:
        tuple: JSON response and status code indicating the application is running.
    """
    logger.info(request)
    return (
        jsonify("App is running"),
        200,
    )


@bp.route("/user/<string:id>", methods=["GET"])
@validate_timestamp_id
def retrieve_user_details(id):
    """
     Endpoint to retrieve user details by ID.
    Args:
        id (str): The user ID.
    Returns:
        tuple: JSON response with user data or error message and status code.
    """
    logger.info(request)
    user_data = retrieve_document_from_collection(str(id))
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404


@bp.route("/user", methods=["POST"])
@validate_json(["id", "first_name", "email", "age", "address"])
@validate_email("email")
@validate_string_length("first_name", min_length=2, max_length=50)
@validate_numeric("age", min_value=18, max_value=99)
@validate_address("address")
def store_user_details():
    """
    Endpoint to store user details.

    The request body should include:
        - id (str): The user ID.
        - first_name (str): The user's first name.
        - last_name (str): The user's last name.
        - age (int): The user's age.
        - email (str): The user's email address.
        - address (dict): The user's address.

    Returns:
        tuple: JSON response with the added document or error message and status code.
    """
    logger.info(request)
    # Retrieve the request body as a dictionary
    request_body = request.get_json()
    document = {
        "id": str(request_body.get("id")),
        "first_name": request_body.get("first_name"),
        "last_name": request_body.get("last_name"),
        "age": request_body.get("age"),
        "email": request_body.get("email"),
        "address": request_body.get("address"),
    }

    added_document = add_document_to_collection(document)
    if added_document:
        return jsonify(added_document), 201
    else:
        return jsonify({"message": "Failed to add document"}), 500
