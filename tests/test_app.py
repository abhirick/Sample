import unittest
from unittest.mock import patch, Mock
from flask import json
from app import create_app


class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_status_check(self):
        response = self.client.get("/user/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), "App is running")

    def test_retrieve_user_details_success(self):

        response = self.client.get("/user/1720955324766")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/user/1720959029188")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["first_name"], "Abhishek")
        self.assertEqual(response.get_json()["last_name"], "Mallick")

    def test_retrieve_user_details_error(self):

        response = self.client.get("/user/123")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"message": "User not found"})

    def test_retrieve_user_details_validation_failure(self):

        response = self.client.get("/user/2720955324766")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "ID is not a valid timestamp"})

    def test_store_user_details_success(self):
        user_data = {
            "id": "1",
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "email": "john.doe@example.com",
            "address": {
                "street": "123 Main St",
                "city": "Halifax",
                "state": "Yorkshire",
                "zip": "HX1 0AB",
            },
        }

        response = self.client.post(
            "/user", data=json.dumps(user_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_store_user_details_validation_failure(self):
        user_data = {
            "id": "1",
            "first_name": "",
            "last_name": "Doe",
            "age": 30,
            "email": "john.doe@example.com",
            "address": {
                "street": "123 Main St",
                "city": "Halifax",
                "state": "Yorkshire",
                "zip": "HX1 0AB",
            },
        }

        response = self.client.post(
            "/user", data=json.dumps(user_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Field 'first_name' must be between 2 and 50 characters long"},
        )

        user_data = {
            "id": "1",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "address": {
                "street": "123 Main St",
                "city": "Halifax",
                "state": "Yorkshire",
                "zip": "HX1 0AB",
            },
        }

        response = self.client.post(
            "/user", data=json.dumps(user_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Missing fields: age"},
        )

        user_data = {
            "id": "1",
            "first_name": "John",
            "last_name": "Doe",
            "age": 0,
            "email": "john.doe@example.com",
            "address": {
                "street": "123 Main St",
                "city": "Halifax",
                "state": "Yorkshire",
                "zip": "HX1 0AB",
            },
        }

        response = self.client.post(
            "/user", data=json.dumps(user_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Field 'age' must be between 18 and 99"},
        )


if __name__ == "__main__":
    unittest.main()
