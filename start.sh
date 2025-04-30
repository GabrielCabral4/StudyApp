#!/bin/bash

# Get the port from Railway or use default
PORT=${PORT:-8000}

# Start Gunicorn with the correct port
exec gunicorn StudyLife_Partner.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -