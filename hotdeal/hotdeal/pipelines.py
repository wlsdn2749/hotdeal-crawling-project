# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re

class HotdealPipeline:
    def open_spider(self, spider):
        spider.logger.info("TestSpider Pipelines Started.")
        
    def process_item(self, item, spider):
        # recommend 필드 처리
        
        if item['recommend'] is None:
            item['recommend'] = '0'
        item['recommend'] = re.sub(r'[\[\]]', '', item['recommend'])

        # comment 필드 처리
        if item['comment'] is None:
            item['comment'] = '0'
        item['comment'] = re.sub(r'[\[\]]', '', item['comment'])

        # url, site 필드 처리
        item['url'] = "https://www.fmkorea.com" + item['url']
        item['site'] = item['site'].strip()
        
        # title 필드 처리
        
        item['title'] = item['title'].strip()

        # time 필드 처리
        item['time'] = item['time'].strip()

        # author 필드 처리
        item['author'] = re.sub(r'[\s/]', '', item['author'])

        return item

class HotdealDetailPipeline:
    def open_spider(self, spider):
        spider.logger.info("TestSpider HotdealDetail Pipelines Started.")
        
    def process_item(self, item, spider):
        # shoppingmall field 처리
        
        item['shoppingmall'] = item['shoppingmall'].strip()
        
        if item['article'] is None:
            item['article'] = ""
            
        return item
