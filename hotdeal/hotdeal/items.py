# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from dataclasses import dataclass

@dataclass
class HotdealItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    recommend: str
    title: str
    comment: str
    shoppingmall: str
    price: str
    deliveryfee: str
    category: str
    time: str
    author: str
