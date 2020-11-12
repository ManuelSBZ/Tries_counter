#!/bin/sh

flask db init
flask db migrate 
flask db upgrade
gunicorn entrypoint:apk -w 2 --threads 2 -b 0.0.0.0:7070

exec "$@"