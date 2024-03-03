#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python phihra/manage.py collectstatic --no-input
python phihra/manage.py migrate