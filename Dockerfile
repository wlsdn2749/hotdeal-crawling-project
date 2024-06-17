FROM python:3.12

WORKDIR /test_app

RUN apt-get update && \
    apt-get install -y uvicorn

RUN pip install poetry

COPY pyproject.toml .
COPY api ./api/

RUN poetry install --no-root

CMD ["poetry","run","uvicorn","api.main:app","--reload","--host","0.0.0.0","--port","8000"]
EXPOSE 8000
