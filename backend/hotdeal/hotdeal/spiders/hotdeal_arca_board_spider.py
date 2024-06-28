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

class ArcaBoardSpider(scrapy.Spider):
    name = "arca_hotdeal_board" # Spider 식별자, Unique 해야함
    custom_settings = {
        'ITEM_PIPELINES': {
            "hotdeal.pipelines.HotdealDetailPipeline": 300,
        },
        'FEEDS': {
            f'{FEED_PATH}/arca_hotdeal_board.csv': {
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
        self.site = "arca"
    
    def get_urls(self):
    
        self.conn.execute(f"CREATE TABLE arca AS SELECT * FROM read_csv_auto('{FEED_PATH}/arca_hotdeal.csv')")
        query = f"""
            SELECT url
            FROM arca
        """
        
        result = self.conn.execute(query).fetchall()
        
        urls = [str(url[0]) for url in result]
        return urls
        
    def start_requests(self):
        # urls = [
        #     "https://arca.live/b/hotdeal/109073306?p=1",
        #     "https://arca.live/b/hotdeal/109073064?p=1"
        # ]
        
        urls = self.urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) 
            # url에 요청날려~
            
    def parse(self, response):
        
        comments_lst = []
        idx = 0
        while True:
            idx += 1
            comments = response.xpath(f"//div[contains(@class, 'article-comment position-relative')]/div[contains(@class, 'list-area')]/div[{idx}]//div[contains(@class, 'content')]")
            
            if not comments:
                break
            
            comments_lst.append({
                "author": comments.xpath(".//span[contains(@class, 'user-info')]/a/text()").get(),
                "date": comments.xpath(".//time/@datetime").get(),
                "content": comments.xpath(".//div[contains(@class, 'message')]//pre/text()").get()
            })
            
        base = response.xpath("//div[contains(@class, 'article-wrapper')]")
        
        title_row = base.xpath("./div[contains(@class, 'article-head')]/div[contains(@class, 'title-row')]")
        info_row = base.xpath("./div[contains(@class, 'article-head')]/div[contains(@class, 'info-row')]")
        table = base.xpath(".//div[contains(@class, 'article-body')]/table[contains(@class, 'table align-middle')]")
        
        yield {
            "site": self.site,
            "url": response.url,
            # "category": title_row.xpath(".//span[contains(@class, 'badge')]/text()").get()
            "title": title_row.xpath(".//div[contains(@class, 'title')]/text()[last()]").get(),
            "date": info_row.xpath(".//div[contains(@class, 'article-info')]/span[contains(@class, 'date')]//time/@datetime").get(),
            "author": info_row.xpath(".//span[contains(@class, 'user-info')]//a/text()").get(),
            "views": info_row.xpath(".//div[contains(@class, 'article-info')]//span[11]/text()").get(),
            "likes": info_row.xpath(".//div[contains(@class, 'article-info')]//span[2]/text()").get(),
            # "dislike": info_row.xpath("//div[contains(@class, 'article-info')]//span[4]/text()").get()
            "comment_count" : info_row.xpath(".//div[contains(@class, 'article-info')]//span[contains(@class, 'body comment-count')]/text()").get(),
            
            "related_url": table.xpath(".//tr[1]//a/text()").get(),
            "shoppingmall": table.xpath(".//tr[2]/td[2]/span/text()").get(),
            "product_name": table.xpath(".//tr[3]/td[2]/span/text()").get(),
            "price": table.xpath(".//tr[4]/td[2]/span/text()").get(),
            "deliveryfee": table.xpath(".//tr[5]/td[2]/span/text()").get(),
            "article": base.xpath("./div[contains(@class, 'article-body')]//div[contains(@class, 'fr-view article-content')]//p[not(a/img)]/text()").getall() ,
            "comments": comments_lst ,
        }