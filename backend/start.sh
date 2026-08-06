#!/bin/sh
echo "================================="
echo "METHYLOX DATABASE MIGRATION CHECK"
echo "================================="
alembic current
echo "================================="
echo "MIGRATION HISTORY"
echo "================================="
alembic history
echo "================================="
echo "STARTING METHYLOX API"
echo "================================="
uvicorn app.main:app --host 0.0.0.0 --port 8000
