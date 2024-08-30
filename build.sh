#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
py manage.py makemigrations --noinput
py manage.py migrate --noinput
py manage.py collectstatic --noinput --clear