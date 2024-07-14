# User Details Application

## Overview
This is a Flask-based Python application designed to manage user details. It provides endpoints to check application status, retrieve user details, and store user details in Firestore.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Docker Setup](#docker-setup)
- [Deploying to Cloud Run using Cloud Build](#deploying-to-cloud-run-using-cloud-build)
- [API Endpoints](#api-endpoints)
- [Sample Images](#sample-images)

## Features
- **Status Check:** Endpoint to check if the application is running.
- **Retrieve User Details:** Endpoint to retrieve user details by user ID.
- **Store User Details:** Endpoint to store user details.

## Requirements
- Python 3.8+
- Flask
- Firebase Admin SDK
- Google Cloud Firestore

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-repo/user_details_app.git
   cd user_details_app
2. Create a Virtual Environment and Activate it:
   ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install the Required Packages:
   ```sh
     pip install -r requirements.txt
4. Set Up Environment Variables:
   Ensure you have your GOOGLE_APPLICATION_CREDENTIALS set to your service account JSON file.
   ```sh
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"

## Configuration
   Update the configuration settings in the config.py and config.ini file as required.
   ```sh
         [default]
         HOST = 0.0.0.0
         PORT = 5000
         COLLECTION = users
   ```

## Running the Application
   To run the Flask application locally
   ```sh
         GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json python3 run.py
   ```

## Running Tests
To run unit tests for the application: 
```sh
  GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json python3 -m unittest discover -s tests
```

## Docker Setup
1. Build the Docker Image.
   ```sh
   docker build -t flask-app . 

2. Run the Docker Container.
   ```sh
   docker run -p 5000:5000 flask-app
   docker run -p 5000:5000 -e GOOGLE_APPLICATION_CREDENTIALS="/path/in/container/serviceAccountKey.json" flask-app
   ```

3. Access the Application.
     The application will be accessible at http://localhost:5000/


## Deploying to Cloud Run using Cloud Build
1. Create cloudbuild.yaml:
 ```sh
 steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/flask-app', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/flask-app']
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  entrypoint: 'gcloud'
  args: [
  'run', 'deploy', 'flask-app',
  '--image', 'gcr.io/$PROJECT_ID/flask-app',
  '--platform', 'managed',
  '--region', 'us-central1',
  '--allow-unauthenticated',
  '--port', '5000',
  '--set-env-vars', 'GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/serviceAccountKey.json'
]

images:
- 'gcr.io/$PROJECT_ID/flask-app'
 ```
2. Submit Build to Cloud Build:
   ```sh
      gcloud builds submit --config cloudbuild.yaml .
   ```
## API Endpoints
   1. Status Check
      URL: /user/status
      Method: GET
      Response:
      ```sh
      {
        "message": "App is running"
      }
      ```
   2. Retrieve User Details
      URL: /user/<string:id>
      Method: GET
      Response:
      ```sh
      {
        "id": "1",
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "address": {
          "street": "123 Main St",
          "city": "Halifax",
          "state": "Yorkshire",
          "zip": "HX1 0AB"
        }
      }
    ```
   3. Store User Details
      URL: /user
      Method: POST
      Request Body:
      ```sh
      {
        "id": "1",
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "address": {
          "street": "123 Main St",
          "city": "Halifax",
          "state": "Yorkshire",
          "zip": "HX1 0AB"
        }
      }
      ```
      Response:
      ```sh
      {
        "id": "1"
      }
      ```
