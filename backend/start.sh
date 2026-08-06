#!/bin/sh

echo "================================="
echo "METHYLOX DATABASE MIGRATION"
echo "================================="

alembic upgrade head

echo "================================="
echo "STARTING METHYLOX API"
echo "================================="

uvicorn app.main:app --host 0.0.0.0 --port 8000
