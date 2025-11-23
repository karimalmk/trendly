#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# If a port is provided, use it; otherwise default to 8000
PORT=${1:-8000}

# Run Django server
python manage.py runserver 0.0.0.0:$PORT
