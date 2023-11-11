#!/bin/sh

while ! nc -z db 3306;
do
    echo "Waiting for the MySQL Server"
    sleep 3
done
echo "Site is running..."
gunicorn app:app --bind 0.0.0.0:5000 --timeout 90 --workers 3
