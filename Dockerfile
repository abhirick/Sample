# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt ./

# Upgrade pip and install dependencies with SSL verification disabled
RUN python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the service account key file into the container
COPY serviceAccountKey.json /usr/src/app/

# Set environment variable for the service account path
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/serviceAccountKey.json

# Expose the port that the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]
