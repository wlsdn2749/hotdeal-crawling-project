# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from hotdeal.utils import convert_to_datetime, convert_to_datetime_detail
import pickle
import re
import base64


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

        """
            Time Field Process
            
            Input 1 = HH:MM
            Input 2 = YYYY.MM.DD
            
            Output -> YYYY-MM-DD HH:MM
        """
        item['time'] = convert_to_datetime(item['time'].strip())

        # author 필드 처리
        item['author'] = re.sub(r'[\s/]', '', item['author'])

        return item

class HotdealDetailPipeline:
    def open_spider(self, spider):
        spider.logger.info("TestSpider HotdealDetail Pipelines Started.")
        
    def process_item(self, item, spider):
        # shoppingmall field 처리
        
        item['shoppingmall'] = item['shoppingmall'].strip()
        
        # article이 아예 없는 경우
        if item['article'] is None:
            item['article'] = ""
        
        for comments in item['comments']:
            comments['author'] = comments['author'].strip()
            comments['content'] = [content.strip() for content in comments['content']]
            comments['date'] = convert_to_datetime_detail(comments['date'].replace(" ", "")) 
            
        item['comments'] = base64.b64encode(pickle.dumps(item['comments'])).decode('utf-8') # pickle로 comment data 직렬화 -> base64 encoding
        
            
        return item
