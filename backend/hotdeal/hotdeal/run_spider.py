import sys
import os
import logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import asyncioreactor, defer
from twisted.internet.task import react

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 크롤러 모듈 임포트
from spiders.hotdeal_qz_spider import QzSpider
from spiders.hotdeal_arca_spider import ArcaSpider
from spiders.hotdeal_ruli_spider import RuliSpider

from spiders.hotdeal_qz_board_spider import QzBoardSpider
from spiders.hotdeal_arca_board_spider import ArcaBoardSpider
from spiders.hotdeal_ruli_board_spider import RuliBoardSpider

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/var/log/spiders/spider_activity.log")
    ]
)
logger = logging.getLogger('spider_runner')

def run_spider(runner, spider):
    return runner.crawl(spider)

@defer.inlineCallbacks
def run_spiders(reactor):
    # Scrapy 프로젝트 설정 가져오기
    settings = get_project_settings()
    
    # Scrapy의 기본 로깅 비활성화
    settings.update({
        'LOG_ENABLED': False,
        'LOG_LEVEL': 'ERROR',  # 에러만 로깅 (필요시)
    })
    
    # 크롤러 러너 초기화 및 설정 업데이트
    runner = CrawlerRunner(settings)

    # 실행할 스파이더들의 리스트
    spiders_to_run = [QzSpider, ArcaSpider, RuliSpider, QzBoardSpider, ArcaBoardSpider, RuliBoardSpider]

    logger.info("Starting spider execution")
    for spider in spiders_to_run:
        logger.info(f"Starting spider: {spider.__name__}")
        yield run_spider(runner, spider)
        logger.info(f"Finished spider: {spider.__name__}")
    logger.info("All spiders finished")

if __name__ == "__main__":
    react(run_spiders)