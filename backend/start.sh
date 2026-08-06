#!/bin/sh
echo "RESETTING MIGRATION STATE..."
alembic stamp base
alembic upgrade head
echo "Starting METHYLOX API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
