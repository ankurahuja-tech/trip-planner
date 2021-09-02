FROM python:3.9-slim-buster

LABEL maintainer="AnkurAhuja.TECH@gmail.com"
LABEL description="Heroku Production image for Trip Planner app"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0

# Install apt-packages, "-y" ensures that there is no user prompt ("yes" to all questions)
RUN apt-get update && apt-get install -y \
    # meta-package - dependencies for building Python packages 
    build-essential \
    # postgresql / psycopg2 dependencies
    libpq-dev \
    # geodjango
    binutils libproj-dev libgdal-dev gdal-bin python-gdal python3-gdal \
    # cleaning up unused files
    && apt-get clean

# Set a working directory
WORKDIR /app

# Copy and install requirements for local development, "-m" flag so it is run as a script
COPY ./requirements /app/requirements
COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt

# Copy project files to docker image
COPY . /app

# run the collectstatic during buildtime so the folder persists;
# see: # https://stackoverflow.com/questions/59719175/where-to-run-collectstatic-when-deploying-django-app-to-heroku-using-docker
RUN python manage.py collectstatic --noinput

# add and run as non-root user with ownership of /app directory
RUN useradd -m user && \
    chown user /app
USER user