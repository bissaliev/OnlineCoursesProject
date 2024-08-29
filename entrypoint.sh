#!/usr/bin/env bash

python manage.py collectstatic --no-input
exec gunicorn --bind 0:8000 product.wsgi