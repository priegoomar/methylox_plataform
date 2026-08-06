#!/bin/sh
echo "FIXING DATABASE MIGRATION STATE..."
alembic stamp 001_add_hospital_isolation
alembic upgrade head
echo "Starting METHYLOX API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
