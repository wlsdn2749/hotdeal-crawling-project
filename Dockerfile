FROM python:3.12

RUN pip install poetry

COPY pyproject.toml poetry.lock .env ./

RUN poetry install --no-root
