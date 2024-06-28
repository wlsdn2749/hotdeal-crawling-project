from pathlib import Path
from typing import Iterable
import scrapy
import duckdb

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import DataUtils

PROJECT_ROOT_PATH = DataUtils.get_current_development()

FEED_PATH = f'{PROJECT_ROOT_PATH}/app/static'

class RuliBoardSpider(scrapy.Spider):
    name = "ruli_hotdeal_board" # Spider 식별자, Unique 해야함
    custom_settings = {
        'ITEM_PIPELINES': {
            "hotdeal.pipelines.HotdealDetailPipeline": 300,
        },
        'FEEDS': {
            f'{FEED_PATH}/ruli_hotdeal_board.csv': {
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
        self.conn = duckdb.connect()
        self.urls = self.get_urls()
        self.site = "ruli"
    
    def get_urls(self):
    
        self.conn.execute(f"CREATE TABLE fm AS SELECT * FROM read_csv_auto('{FEED_PATH}/ruli_hotdeal.csv')")
        query = f"""
            SELECT url
            FROM fm
        """
        
        result = self.conn.execute(query).fetchall()
        
        urls = [str(url[0]) for url in result]
        return urls
        
    def start_requests(self):
        # urls = [
        #     "https://bbs.ruliweb.com/market/board/1020/read/86688",
        # ]
        
        urls = self.urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) 
            # url에 요청날려~
        
    # TODO
    def parse(self, response):
        
        comments_lst = []
        idx = 0
        while True:
            idx += 1
            comments = response.xpath(f".//tr[contains(@class, 'comment_element normal')][{idx}]")
            
            if not comments:
                break
            
            comments_lst.append({
                "author": comments.xpath("./td[contains(@class, 'user')]//strong/span/text()").get(),
                "date": comments.xpath(".//span[contains(@class, 'time')]/text()").get(), #TODO strip()
                "content": comments.xpath("./td[contains(@class, 'comment')]//span[contains(@class, 'text')]/text()").get()
            })
        
        subject =  response.xpath("//div[contains(@class, 'subject')]")
        user = response.xpath("//div[contains(@class, 'col user_info_wrapper')]")
        
        yield {
            "site": self.site,
            "url": response.url,
            # "category": subject.xpath(".//span[contains(@class, 'category_text')]/text()").get() # TODO Strip(), remove parentheses
            "title": subject.xpath(".//span[contains(@class, 'subject_inner_text')]/text()").get(), # TODO strip()
            "date": user.xpath(".//span[contains(@class, 'regdate')]/text()").get(), # %y.%m.%d (%H:%M:%S),
            "author": user.xpath(".//a[contains(@class, 'nick')]/text()").get(), #TODO strip()
            "views":  user.xpath(".//p[text()[contains(., '조회')]]/text()[contains(., '조회')]").get(), #TODO remove \t, 조회, strip()
            "likes": user.xpath(".//span[contains(@class, 'like')]/text()").get(),
            "comment_count" : subject.xpath(".//strong[contains(@class, 'reply_count')]/text()").get(), #TODO remove parentheses,
            "related_url": response.xpath("//div[contains(@class, 'source_url box_line_with_shadow')]/a/@href").get(), #TODO 없으면 미제공 처리해야함,
            "shoppingmall": "lazy", # TODO extract from title
            "product_name": "lazy", # TODO strip(), remove '/' 
            "price": "lazy",
            "deliveryfee": "lazy",                
            "article": "lazy", # Js로 본문을 Load함으로 미구현
            "comments": comments_lst
        }