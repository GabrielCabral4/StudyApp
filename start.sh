#!/bin/bash
exec gunicorn StudyLife_Partner.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120