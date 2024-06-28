cron
service cron restart
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 --root-path /api/v1
