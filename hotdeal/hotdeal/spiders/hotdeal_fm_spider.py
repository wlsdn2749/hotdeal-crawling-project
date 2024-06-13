from pathlib import Path
from typing import Iterable
import scrapy

class QuoteSpider(scrapy.Spider):
    name = "fm_hotdeal" # Spider 식별자, Unique 해야함
    custom_settings = {
        'ITEM_PIPELINES': {
            "hotdeal.pipelines.HotdealPipeline": 300,
        }
    }
    def __init__(self):
        self.site = "fm"
        
    def start_requests(self):
        # urls = [
        #     "https://www.fmkorea.com/hotdeal",
        # ]
        
        urls = [
            f"https://www.fmkorea.com/index.php?mid=hotdeal&page={idx}" for idx in range(10)
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) 
            # url에 요청날려~
            
    def parse(self, response):
        
        for quote in response.xpath("//li[contains(@class, 'li  li_best2_pop0 li_best2_hotdeal0')]"):
            yield {
                "site": self.site,
                "url": quote.xpath(".//a/@href").get(),
                "recommend": quote.xpath(".//span[contains(@class, 'count')]/text()").get(),
                "title": quote.xpath(".//a[contains(@class, 'hotdeal_var8')]/text()").get(),
                "comment": quote.xpath(".//span[contains(@class, 'comment_count')]/text()").get(),
                "shoppingmall": quote.xpath(".//div[contains(@class, 'hotdeal_info')]//span[contains(text(), '쇼핑몰')]/a/text()").get(),
                "price": quote.xpath(".//div[contains(@class, 'hotdeal_info')]//span[contains(text(), '가격')]/a/text()").get(),
                "deliveryfee": quote.xpath(".//div[contains(@class, 'hotdeal_info')]//span[contains(text(), '배송')]/a/text()").get(),
                "category": quote.xpath(".//span[contains(@class, 'category')]/a/text()").get(),
                "time": quote.xpath(".//span[contains(@class, 'regdate')]/text()").get(),
                "author": quote.xpath(".//span[contains(@class, 'author')]/text()").get(),
            }