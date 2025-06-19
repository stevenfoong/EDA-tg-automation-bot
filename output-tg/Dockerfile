# Use Python 3.11 as the base image
# FROM python:3.9-slim
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your application code into the container
COPY . /app

# Run the bot script when the container starts
CMD ["python", "-u", "output-tg.py"]

