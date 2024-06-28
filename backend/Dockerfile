FROM python:3.12

WORKDIR /backend

RUN apt-get update && \
    apt-get install -y uvicorn cron && \
    apt-get clean

RUN pip install poetry

COPY pyproject.toml .
COPY app ./app/
COPY hotdeal ./hotdeal
COPY run_spider /etc/cron.d/run_spider
COPY run.sh .

RUN poetry config virtualenvs.in-project true
RUN poetry config virtualenvs.path "./.venv"

RUN mkdir /var/log/spiders
RUN touch /var/log/spiders/spider_activity.log
RUN chmod 0666 /var/log/spiders/spider_activity.log
RUN chown root:root /var/log/spiders/spider_activity.log

RUN chmod +x /backend/hotdeal/hotdeal/run_spider.py

RUN chmod 0644 /etc/cron.d/run_spider
RUN chmod 0755 ./run.sh

RUN poetry install --no-root && poetry update

CMD ["/bin/sh","./run.sh"]
EXPOSE 8001
