import scrapy

class QzSpider(scrapy.Spider):
    name = "qz_hotdeal"
    custom_settings = {
        'ITEM_PIPELINES': {
            "hotdeal.pipelines.HotdealPipeline": 300,
        },
        'FEEDS': {
            '/workspace/hotdeal-crawling-project/backend/app/static/qz_hotdeal.csv': {
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
        self.site = "qz"
        
    def start_requests(self):
        print(f"Crawl Start {self.site} ")
        urls = [
            f'https://quasarzone.com/bbs/qb_saleinfo?page={idx}' for idx in range(1, 6)
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        
        base = response.xpath("//div[contains(@class, 'market-type-list market-info-type-list relative')]/table/tbody/tr")
        
        for qz in base:            
            
            tit = qz.xpath(".//p[contains(@class, 'tit')]")
            market_info_sub = qz.xpath(".//div[contains(@class, 'market-info-sub')]")   
            
            yield { 
                "site": self.site,
                "url": tit.xpath(".//a/@href").get(),
                "recommend": qz.xpath("./td[1]/span[contains(@class, 'num')]/text()").get(),
                "title": tit.xpath("./a/span/text()").get(),
                "comment": tit.xpath(".//span[contains(@class, 'ctn-count')]/text()").get(),
                "shoppingmall": "lazy",
                "price": market_info_sub.xpath(".//span[contains(text(), '가격')]/span/text()").get(),
                "deliveryfee": market_info_sub.xpath("./p/span[last()]/text()").get() ,
                "category": market_info_sub.xpath(".//span[contains(@class, 'category')]/text()").get(),
                "time": market_info_sub.xpath(".//span[contains(@class, 'date')]/text()").get(),
                "author": market_info_sub.xpath(".//span[contains(@class, 'user-nick-wrap nick')]/@data-nick").get() ,
                "views": market_info_sub.xpath(".//span[contains(@class, 'count')]/text()").get()
            }