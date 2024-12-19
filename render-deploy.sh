#!/usr/bin/env bash
set -e

poetry install --no-root
poetry run flask --app src.hello db upgrade
poetry run gunicorn src.wsgi:app