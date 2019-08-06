#!/bin/bash

#Ensure staticfiles are present
exec python3.6 /app/manage.py collectstatic

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn api.wsgi:application \
    --bind 0.0.0.0:5000 \
    --workers 3
