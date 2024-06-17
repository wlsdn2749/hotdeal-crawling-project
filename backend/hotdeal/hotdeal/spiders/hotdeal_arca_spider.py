import scrapy


class ArcaSpider(scrapy.Spider):
    name = "arca_hotdeal"
    custom_settings = {
        'ITEM_PIPELINES': {
            "hotdeal.pipelines.HotdealPipeline": 300,
        }
    }
    def __init__(self):
        self.site = "arca"
        
    def start_requests(self):
        urls = [
            'https://arca.live/b/hotdeal?p=1'
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        
        base = response.xpath("//div[contains(@class, 'list-table hybrid')]//div[contains(@class, 'vrow hybrid')]")
        
        for arca in base:            
            
            col_title = arca.xpath(".//span[contains(@class, 'vcol col-title')]//span[contains(@class, 'badges')]")
            vrow_bottom = arca.xpath(".//div[contains(@class, 'vrow-bottom deal')]")   
            
            yield { 
                "site": self.site,
                "url": arca.xpath(".//a[contains(@class, 'title hybrid-title')]/@href").get(),
                "recommend": vrow_bottom.xpath(".//span[contains(@class, 'vcol col-rate')]/text()").get(),  
                "title": arca.xpath(".//a[contains(@class, 'title hybrid-title')]/text()[2]").get(),
                "comment": arca.xpath(".//a[contains(@class, 'title hybrid-title')]//span[contains(@class, 'comment-count')]/text()").get(),
                "shoppingmall": col_title.xpath(".//span[contains(@class, 'deal-store')]//text()").get(),
                "price": vrow_bottom.xpath(".//span[contains(@class, 'deal-price')]/text()").get(),
                "deliveryfee": vrow_bottom.xpath(".//span[contains(@class, 'deal-delivery')]/text()").get(),
                "category": col_title.xpath(".//a[contains(@class, 'badge')]//text()").get(),
                "time": vrow_bottom.xpath(".//span[contains(@class, 'vcol col-time')]/time/@datetime").get(),
                "author": vrow_bottom.xpath(".//span[contains(@class, 'user-info')]/span/@data-filter").get(),
                "views": vrow_bottom.xpath(".//span[contains(@class, 'vcol col-view')]/text()").get()
            }
        
