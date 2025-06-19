# Path: frontend/Dockerfile

# Use the same base Python image for consistency
FROM python:3.10-slim

# Set the working directory inside this container
WORKDIR /app

# Copy the requirements file from the root directory and install dependencies
# The '..' allows us to go up one level to find the requirements.txt
COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy only the frontend application code into the container
COPY . /app

# The port Streamlit will run on inside the container
EXPOSE 8080

# The command to start the Streamlit app
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8080", "--server.address=0.0.0.0"]