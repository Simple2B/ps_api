#!/bin/sh

echo Run API server
.venv/bin/uvicorn --workers 4 --host 0.0.0.0 --port $APP_PORT api:api
