#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Optional: set Django settings module (uncomment if needed)
# export DJANGO_SETTINGS_MODULE=trendly.settings

# Run Django development server
python manage.py runserver 0.0.0.0:8000