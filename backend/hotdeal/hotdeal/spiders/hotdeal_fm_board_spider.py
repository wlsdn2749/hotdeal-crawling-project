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

class QuoteSpider(scrapy.Spider):
    name = "fm_hotdeal_board" # Spider 식별자, Unique 해야함
    custom_settings = {
        'ITEM_PIPELINES': {
            "hotdeal.pipelines.HotdealDetailPipeline": 300,
        }
    }
    
    def __init__(self):
        self.conn = duckdb.connect()
        self.urls = self.get_urls()
    
    def get_urls(self):
    
        self.conn.execute("CREATE TABLE fm AS SELECT * FROM read_csv_auto('./hotdeal.csv')")
        query = f"""
            SELECT url
            FROM fm
        """
        
        result = self.conn.execute(query).fetchall()
        
        urls = [str(url[0]) for url in result]
        return urls
        
    def start_requests(self):
        # urls = [
        #     "https://www.fmkorea.com/hotdeal",
        #     "https://www.fmkorea.com/7144685181"
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
            comments = response.xpath(f"//div[contains(@class, 'rd rd_nav_style2 clear')]//ul[contains(@class, 'fdb_lst_ul ')]//li[{idx}]")
            
            if not comments:
                break
            
            comments_lst.append({
                "author": comments.xpath(f".//div/a/text()").get(),
                "date": comments.xpath(f".//div/span/text()").get(),
                "content": comments.xpath(f".//div[contains(@class, 'comment-content')]//div/text()").getall()
            })
            
        for quote in response.xpath("//div[contains(@class, 'rd rd_nav_style2 clear')]"):
            yield {
                "site": "fm",
                "url": response.url,
                "title": quote.xpath(".//span[contains(@class, 'np_18px_span')]/text()").get(),
                "date": quote.xpath(".//span[contains(@class, 'date m_no')]/text()").get(),
                "author": quote.xpath(".//div[contains(@class, 'btm_area clear')]//div[contains(@class, 'side')]//a/text()").get(),
                "views": quote.xpath(".//div[contains(@class, 'side fr')]//span[1]/b/text()").get(),
                "likes": quote.xpath(".//div[contains(@class, 'side fr')]//span[2]/b/text()").get(),
                "comment_count" : quote.xpath(".//div[contains(@class, 'side fr')]//span[3]/b/text()").get(),
                
                "related_url":  quote.xpath(".//table[contains(@class, 'hotdeal_table')]//tr[1]//div[contains(@class, 'xe_content')]//a/text()").get(),
                "shoppingmall": quote.xpath("//table[contains(@class, 'hotdeal_table')]//tr[2]//div[contains(@class, 'xe_content')]/text()").get(),
                "product_name": quote.xpath("//table[contains(@class, 'hotdeal_table')]//tr[3]//div[contains(@class, 'xe_content')]/text()").get(),
                "price": quote.xpath("//table[contains(@class, 'hotdeal_table')]//tr[4]//div[contains(@class, 'xe_content')]/text()").get(),
                "deliveryfee": quote.xpath("//table[contains(@class, 'hotdeal_table')]//tr[5]//div[contains(@class, 'xe_content')]/text()").get(),
                "article": response.xpath("//div[contains(@class, 'rd rd_nav_style2 clear')]//article//div[position() > 1]/text()").getall(),
                "comments": comments_lst
            }