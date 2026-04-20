#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python admin_site/manage.py collectstatic --noinput
python admin_site/manage.py migrate
python admin_site/manage.py seed_mock
