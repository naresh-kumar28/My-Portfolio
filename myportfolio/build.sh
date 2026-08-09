#!/usr/bin/env bash
# exit on error
set -o errexit

if [ -d "myportfolio" ]; then
  cd myportfolio
fi

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
