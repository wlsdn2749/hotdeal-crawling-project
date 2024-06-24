from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR

import scrapy
import sys
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import logging
import time
import os

sys.path.append("/workspace/hotdeal-crawling-project/backend/hotdeal/hotdeal/spiders/")
from hotdeal_qz_spider import QzSpider

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_spider(spider: scrapy.Spider):
    settings = get_project_settings()
    updated_settings = update_settings(settings)
    process = CrawlerProcess(updated_settings)
    process.crawl(spider)
    process.start()


def update_settings(settings):
    csv_file = f'{DIR_PATH}/test.csv'
    
    # 기존 설정 유지
    custom_settings = dict(settings)
    
    # CSV 출력 관련 설정 추가
    custom_settings.update({
        'FEEDS': {
            csv_file: {
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': True,
            },
        },
    })
    
    return custom_settings

# 작업 함수들
def job1():
    logger.info("Job 1 시작")
    time.sleep(2)
    logger.info("Job 1 완료")

def job2():
    logger.info("Job 2 시작")
    time.sleep(3)
    logger.info("Job 2 완료")

def job3():
    logger.info("Job 3 시작")
    time.sleep(1)
    raise Exception("Job 3 에러 발생")

def job4():
    logger.info("Job 4 시작")
    time.sleep(4)
    logger.info("Job 4 완료")

# 에러 핸들러
def job_error_handler(event):
    if event.exception:
        logger.error(f"작업 {event.job_id}에서 에러 발생: {event.exception}")
        logger.info(f"다른 작업들은 계속 실행됩니다.")

# 스케줄러 설정
executors = {
    'default': ThreadPoolExecutor(max_workers=4)
}

scheduler = BackgroundScheduler(executors=executors)

scheduler.add_listener(job_error_handler, mask=EVENT_JOB_ERROR)

# 작업 추가
scheduler.add_job(run_spider, 'interval', minutes=60, args=[QzSpider], next_run_time=datetime.now())  # 60분마다 실행
# scheduler.add_job(job1, 'interval', seconds=10, id='job1')
# scheduler.add_job(job2, 'interval', seconds=10, id='job2')
# scheduler.add_job(job3, 'interval', seconds=10, id='job3')
# scheduler.add_job(job4, 'interval', seconds=10, id='job4')

# 스케줄러 시작
scheduler.start()

try:
    # 스케줄러를 계속 실행
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    # 스케줄러 종료
    scheduler.shutdown()