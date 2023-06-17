import scrapy


class ConcavebtSpider(scrapy.Spider):
    name = "concavebt"
    allowed_domains = ["concavebt.com"]
    start_urls = ['https://concavebt.com/top-100-product-placement-brands-in-2022-movies/']

    def parse(self, response):
        a = response
        pass
