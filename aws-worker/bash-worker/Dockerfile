# Use Python 3.11 as the base image
#FROM python:3.9-slim
FROM python:3.11-slim

# Install curl and clean up cache to reduce image size
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your application code into the container
COPY . /app

# Run the bot script when the container starts
CMD ["python", "-u", "bash-worker.py"]


