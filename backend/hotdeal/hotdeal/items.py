# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from dataclasses import dataclass

@dataclass
class HotdealItem(scrapy.Item):

    site: str
    url: str
    recommend: str
    title: str
    comment: str
    shoppingmall: str
    price: str
    deliveryfee: str
    category: str
    time: str
    author: str
    

@dataclass
class HotdealItemDetail(scrapy.Item):
    site: str
    url: str
    title: str
    date: str
    author: str
    views: str
    likes: str
    comment_count: str
    related_url: str
    shoppingmall: str
    product_name: str
    price: str
    deliveryfee: str
    article: str
    comments: str
