from pathlib import Path
from typing import Iterable
import scrapy
import duckdb

FEED_PATH = '/workspace/hotdeal-crawling-project/backend/app/static'

class QzBoardSpider(scrapy.Spider):
    name = "qz_hotdeal_board" # Spider 식별자, Unique 해야함
    custom_settings = {
        'ITEM_PIPELINES': {
            "hotdeal.pipelines.HotdealDetailPipeline": 300,
        },
        'FEEDS': {
            f'{FEED_PATH}/qz_hotdeal_board.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': True,
            },
        },
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 2,
        'LOG_ENABLED': False
    }
    
    def __init__(self):
        self.conn = duckdb.connect()
        self.urls = self.get_urls()
        self.site = "qz"
    
    def get_urls(self):
    
        self.conn.execute(f"CREATE TABLE qz AS SELECT * FROM read_csv_auto('{FEED_PATH}/qz_hotdeal.csv')")
        query = f"""
            SELECT url
            FROM qz
        """
        
        result = self.conn.execute(query).fetchall()
        
        urls = [str(url[0]) for url in result]
        return urls
        
    def start_requests(self):
        # urls = [
        #     "https://quasarzone.com/bbs/qb_saleinfo/views/1616822",
        # ]
        
        urls = self.urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) 
            # url에 요청날려~
        
    # TODO
    def parse(self, response):
        
        comments_lst = []
        # idx = 0
        # while True:
        #     idx += 1
        #     comments = response.xpath(f"//div[contains(@class, 'article-comment position-relative')]/div[contains(@class, 'list-area')]/div[{idx}]//div[contains(@class, 'content')]")
            
        #     if not comments:
        #         break
            
        #     comments_lst.append({
        #         "author": comments.xpath(".//span[contains(@class, 'user-info')]/a/text()").get(),
        #         "date": comments.xpath(".//time/@datetime").get(),
        #         "content": comments.xpath(".//div[contains(@class, 'message')]//pre/text()").get()
        #     })
            
        base = response.xpath("//div[contains(@class, 'common-view-area')]")
        
        top = base.xpath("./dl/dt")
        top_util = top.xpath(".//div[contains(@class, 'util-area')]")
        table = base.xpath("./dl/dd/table[contains(@class, 'market-info-view-table')]")
        
        yield {
            "site": self.site,
            "url": response.url,
            # "category": top_util.xpath(".//div[contains(@class, 'ca_name')]/text()").get() # TODO Strip()
            "title": top.xpath(".//h1[contains(@class, 'title')]/text()[last()]").get(), # TODO strip()
            "date": top_util.xpath(".//span[contains(@class, 'date')]/text()").get(), # %y.%m.%d %H:%M,
            "author": top_util.xpath(".//div[contains(@class, 'user-nick-wrap user')]/@data-nick").get(), #!NEED : Prefix Remove
            "views":  top_util.xpath(".//span[contains(@class, 'count')]//em[contains(@class, 'view')]/text()").get(),
            "likes": top.xpath(".//span[contains(@id, 'boardGoodCount')]/text()").get(), # TODO strip()
            "comment_count" : top_util.xpath(".//span[contains(@class, 'count')]//em[contains(@class, 'reply')]/text()").get(),
            "related_url": table.xpath("./tr[1]//a/text()").get(),
            "shoppingmall": table.xpath("./tr[2]//td/text()[last()]").get(), # TODO strip()
            "product_name": "lazy", # TODO strip(), remove '/' 
            "price": table.xpath("./tr[3]//span/text()[last()]").get(),            
            "deliveryfee": table.xpath("./tr[4]/td/text()").get(),
            "article": response.xpath(".//textarea[contains(@id, 'org_contents')]/p/text()").getall(), 
            "comments": comments_lst # JS로 댓글을 Load함으로 지금 현재 미구현
        }