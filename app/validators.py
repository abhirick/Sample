import re
from flask import request, jsonify
from functools import wraps
from flask import abort
import time


def validate_json(required_fields):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400

            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return (
                    jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}),
                    400,
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_email(field):
    def decorator(f):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            email = data.get(field)
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

            if email and not re.match(email_regex, email):
                return (
                    jsonify({"error": f"Invalid email format for field: {field}"}),
                    400,
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_string_length(field, min_length=1, max_length=255):
    def decorator(f):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            value = data.get(field, "")

            if not (min_length <= len(value) <= max_length):
                return (
                    jsonify(
                        {
                            "error": f"Field '{field}' must be between {min_length} and {max_length} characters long"
                        }
                    ),
                    400,
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_numeric(field, min_value=None, max_value=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            value = data.get(field)

            try:
                value = float(value)
            except (TypeError, ValueError):
                return (
                    jsonify({"error": f"Field '{field}' must be a numeric value"}),
                    400,
                )

            if (min_value is not None and value < min_value) or (
                max_value is not None and value > max_value
            ):
                return (
                    jsonify(
                        {
                            "error": f"Field '{field}' must be between {min_value} and {max_value}"
                        }
                    ),
                    400,
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_range(min_value, max_value):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for key, value in kwargs.items():
                try:
                    if not (min_value <= int(value) <= max_value):
                        abort(
                            400,
                            description=f"{key} must be between {min_value} and {max_value}",
                        )
                except ValueError:
                    abort(400, description=f"{key} must be an integer")
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_address(field):
    def decorator(f):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            address = data.get(field)

            if not isinstance(address, dict):
                raise ValueError("Address should be a dictionary")

            required_fields = ["street", "city", "state", "zip"]
            for addr_attr in required_fields:

                if addr_attr not in address or not address[addr_attr]:
                    return (
                        jsonify(
                            {
                                "error": f"Missing or empty required field: {addr_attr} in address"
                            }
                        ),
                        400,
                    )

                if not isinstance(address[addr_attr], str):
                    return (
                        jsonify({"error": f"{addr_attr} should be a string"}),
                        400,
                    )

                # Additional field-specific validations
                if addr_attr == "zip":
                    if not (address[addr_attr].replace(" ", "")).isalnum() or len(address[addr_attr]) > 8:
                        return (
                            jsonify(
                                {
                                    "error": f"ZIP code should be alphanumeric and less than 8 characters long"
                                }
                            ),
                            400,
                        )

            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_timestamp_id(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract the ID from the URL path
        unique_id = kwargs.get('id')
        # Validate that the ID is a timestamp (milliseconds since epoch)
        try:
            # Check if the ID is an integer and within a reasonable range
            id_int = int(unique_id)
            current_time_ms = int(time.time() * 1000)
             
            # Assuming IDs are not from the far future (e.g., more than 1 year ahead)
            if id_int > current_time_ms or id_int < 0:
                return jsonify({"error": "ID is not a valid timestamp"}), 400

        except ValueError:
            return jsonify({"error": "ID is not a valid integer"}), 400

        return f(*args, **kwargs)
    
    return decorated_function
