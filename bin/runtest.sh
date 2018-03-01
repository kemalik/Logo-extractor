#!/usr/bin/env bash

sleep 10 # wait db init
python manage.py migrate
python manage.py test
