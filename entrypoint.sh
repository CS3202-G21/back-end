#!/bin/sh

python manage.py makemigrations
python manage.py migrate

gunicorn rms_back_end.wsgi:application --bind 0.0.0.0:8000