#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

gunicorn rms_back_end.wsgi:application --bind 0.0.0.0:8000