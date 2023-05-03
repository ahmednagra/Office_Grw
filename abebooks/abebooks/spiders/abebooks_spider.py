from datetime import datetime
from urllib.parse import urljoin

import scrapy

from ..items import AbebooksItem


class AbeBooksSpider(scrapy.Spider):
    name = 'abe'
    start_urls = ['https://www.abebooks.com/servlet/BookstoreSearch']

    custom_settings = {
    'FEEDS': {
        'Abebooks/%(name)s/%(name)s_%(time)s.csv': {
            'format': 'csv',
            # 'encoding' : 'utf-8',
            'fields': ['Country', 'seller_name', 'address', 'phone_No', 'join_date', 'rating', 
                                 'information', 'seller_id', 'seller_url', 'seller_image_url', 'collection_by_User']
                    }
                }
            }
    
    def parse(self, response):
        countries = ['AUS', 'ITA', 'USA']
        for country in countries:
            formdata = {
                'ph': '2',
                'cm_sp': 'SearchF-_-sellers-_-Results',
                'name': '',
                'country': country,
                'postalcode': ''
            }
            yield scrapy.FormRequest(
                url='https://www.abebooks.com/servlet/BookstoreSearch',
                formdata=formdata,
                callback=self.parse_sellers,
                meta={'country': country}
            )
        
    def parse_sellers(self, response):
        seller_links = response.css('#search-results-target > li > strong > a::attr(href)').getall()
        print('seller_links' , len(seller_links))
        
        for seller_link in seller_links:
            yield scrapy.Request(
                url=seller_link,
                callback=self.parse_seller_detail,
                meta=response.meta
            )

        next_page_url = response.css('a#bottombar-page-next::attr(href)').get()
        if next_page_url:
            full_next_page_url = urljoin(response.url, next_page_url)
            yield scrapy.Request(
                url=full_next_page_url,
                callback=self.parse_sellers,
                meta=response.meta
            )

    def parse_seller_detail(self, response):
        item = AbebooksItem()

        item['Country'] = response.meta['country']
        item['seller_name'] = response.css('div.seller-location h1::text').extract_first().strip()
        # item['address'] = response.css('p.icon.addy::text ').extract_first().strip()
        item['address'] = ''.join(part.strip() for part in response.css('p.icon.addy *::text').extract() if part.strip())
        item['phone_No'] = response.css('p.icon.telly::text ').get()
        item['join_date'] = datetime.strptime(response.css('p.date-joined::text').get().replace('Joined', '').strip(), '%B %d, %Y').strftime('%d:%m:%Y')
        item['rating'] = response.css('.seller-location.indent div a img::attr(alt)').get().replace('-star rating', '')
        item['information'] = response.css('.panel-body.seller-content p::text').get()
        item['seller_id'] = response.css('link[rel="canonical"]::attr(href)').get().split('/')[-2]
        item['seller_url'] = response.css('link[rel="canonical"]::attr(href)').get()
        item['seller_image_url'] = response.css('#main > div.seller-info.liquid-static-col > img::attr(src)').get()
        collection_by_User_link = response.css('#seller-collections div div a img::attr(src)').getall()
        values = response.css('.card-block.text-center h4::text, .card-block.text-center p small::text').getall()
        item['collection_by_User'] = {f"{values[i]}_{values[i+1]}": collection_by_User_link[i//2] for i in range(0, len(values)-1, 2)}

        yield item