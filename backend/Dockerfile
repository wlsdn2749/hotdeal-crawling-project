FROM python:3.12

WORKDIR /backend

RUN apt-get update && \
    apt-get install -y uvicorn cron && \
    apt-get clean

RUN pip install poetry

COPY pyproject.toml .
COPY app ./app/
COPY hotdeal ./hotdeal

RUN poetry config virtualenvs.in-project true
RUN poetry config virtualenvs.path "./.venv"

RUN mkdir /var/log/spiders
RUN touch /var/log/spiders/spider_activity.log
RUN chmod 0666 /var/log/spiders/spider_activity.log
RUN chown root:root /var/log/spiders/spider_activity.log

RUN chmod +x /backend/hotdeal/hotdeal/run_spider.py

COPY run_spider /etc/cron.d/run_spider
RUN chmod 0644 /etc/cron.d/run_spider
RUN service cron start
RUN cron

RUN poetry install --no-root && poetry update

CMD ["poetry","run","uvicorn","app.main:app","--reload","--host","0.0.0.0","--port","8001","--root-path","/api/v1"]
EXPOSE 8001
