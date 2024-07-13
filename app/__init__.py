from flask import Flask, jsonify


class ValidationError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def create_app():
    app = Flask(__name__)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    with app.app_context():
        from . import user_request_handler
        app.register_blueprint(user_request_handler.bp)

    return app
