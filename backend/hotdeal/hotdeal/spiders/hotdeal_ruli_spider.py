import scrapy
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import DataUtils

PROJECT_ROOT_PATH = DataUtils.get_current_development()

class RuliSpider(scrapy.Spider):
    name = "ruli_hotdeal"
    custom_settings = {
        'ITEM_PIPELINES': {
            "hotdeal.pipelines.HotdealPipeline": 300,
        },
        'FEEDS': {
            f'{PROJECT_ROOT_PATH}/app/static/ruli_hotdeal.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': True,
            },
        },
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1,
        'LOG_ENABLED': False
    }
    def __init__(self):
        self.site = "ruli"
        
    def start_requests(self):
        print(f"Crawl Start {self.site} ")
        urls = [
            f"https://bbs.ruliweb.com/market/board/1020?page={idx}" for idx in range(1, 6)
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        
        base = response.xpath("//table[contains(@class, 'board_list_table')]//tr[contains(@class, 'table_body blocktarget')]")
        
        for ruli in base:            
            
            yield { 
                "site": self.site,
                "url": ruli.xpath(".//div[contains(@class, 'relative')]//a[contains(@class, 'deco')]/@href").get() ,
                "recommend": ruli.xpath(".//td[contains(@class, 'recomd')]/text()").get(),
                "title": ruli.xpath(".//div[contains(@class, 'relative')]//a[contains(@class, 'deco')]/text()").get() ,
                "comment": ruli.xpath(".//a[contains(@class, 'num_reply')]/span/text()").get(),
                "shoppingmall": "lazy", #TODO title에서 [] 때면됨
                "price": "lazy",
                "deliveryfee": "lazy",
                "category": ruli.xpath(".//td[contains(@class, 'divsn text_over')]/a/text()").get(),
                "time": ruli.xpath(".//td[contains(@class, 'time')]/text()").get(), # TODO strip()
                "author": ruli.xpath(".//td[contains(@class, 'writer text_over')]/a/text()").get(), #TODO strip()
                "views": ruli.xpath(".//td[contains(@class, 'hit')]/text()").get() # TODO strip()
            }
        
