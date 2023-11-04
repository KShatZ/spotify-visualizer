#!/bin/bash

if [ "$FLASK_APP_MODE" == "PROD" ]; then
    echo "[Start Up] Starting Gunicorn, port 8000..."
    gunicorn app:app -w 3 --bind 0.0.0.0:8000 --access-logfile - --error-logfile -
elif [ "$FLASK_APP_MODE" == "DEV" ]; then
    echo "[Start Up] Dev mode..."
    tail -f /dev/null
else
    echo "[Start Up] Wrong FLASK_APP_MODE value, set to 'PROD' or 'DEV'"
    exit 1
fi