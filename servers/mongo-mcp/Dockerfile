# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Assuming mongo-mcp has a requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8002 available to the world outside this container
EXPOSE 8002

# Run the application
# This command needs to be adjusted based on how mongo-mcp is run
# For example, if it's a FastAPI app, it might be: uvicorn main:app --host 0.0.0.0 --port 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]