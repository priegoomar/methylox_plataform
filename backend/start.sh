#!/bin/sh
echo "Updating Alembic state..."
alembic stamp 002_add_patient_hospital_column
echo "Starting METHYLOX API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
