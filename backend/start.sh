#!/bin/sh
echo "Running Alembic migrations..."
echo "CURRENT ALEMBIC VERSION:"
alembic current
echo "AVAILABLE HEAD:"
alembic heads
alembic upgrade head
echo "Starting METHYLOX API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
