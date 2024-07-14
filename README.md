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

## Installation
