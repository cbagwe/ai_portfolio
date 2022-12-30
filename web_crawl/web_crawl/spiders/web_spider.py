import scrapy

class WebSpiderSpider(scrapy.Spider):
    name = 'web_spider'
    start_urls = ['https://36zerovision.com/solution/']

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']//span[@class='text']/text()").extract()
        yield {'quotes': quotes}
