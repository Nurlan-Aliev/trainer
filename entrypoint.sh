#!/bin/sh
set -e

alembic upgrade head

exec uvicorn main:app --host backend --port 8000