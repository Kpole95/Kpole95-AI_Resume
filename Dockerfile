# Use an official, lean Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file and install all necessary packages
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# --- This is the key improvement ---
# Download the spaCy NLP models during the build process
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ru_core_news_sm

# Copy your application's source code into the container
# We do NOT copy the 'models/' folder.
COPY ./api /code/api
COPY ./backend /code/backend
COPY ./config /code/config

# Set the port the container will listen on. 7860 is standard for Hugging Face.
EXPOSE 7860

# The command to run your FastAPI server when the container starts
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]


