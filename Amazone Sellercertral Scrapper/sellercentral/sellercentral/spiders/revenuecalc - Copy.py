import csv
import json
import os

from scrapy import Spider, Request


class RevenuecalcSpider(Spider):
    name = 'revenuecalc'
    allowed_urls = ['https://concavebt.com/top-100-product-placement-brands-in-2022-movies/']


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.records = self.read_input_file()
        self.counter = 0

    def start_requests(self):
        for record in self.records[:1]:
            ean = record['EAN']
            price = record['Price']

        url1 = f'https://sellercentral.amazon.fr/rcpublic/productmatch?searchKey={ean}&countryCode=DE&locale=de-EN'
        yield Request(
            url=url1,
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse,
            meta={'ean': ean, 'price': price}
        )

    def parse(self, response):
        data = self.response_json(response)
        first_product = data.get('data', '').get('otherProducts', '').get('products', '')[0]
        asin = first_product.get('asin', '')
        sale_rank = first_product.get('salesRank', '')

        # url = f'https://sellercentral.amazon.fr/rcpublic/getadditionalpronductinfo?countryCode=DE&asin={asin}&fnsku=&searchType=GENERAL&locale=de-EN'
        url = 'https://sellercentral.amazon.fr/rcpublic/getfees'
        body = self.form_data(asin=asin)
        yield Request(url=url,
                      headers=self.headers,
                      cookies=self.cookies,
                      body=body,
                      method='POST',
                      callback=self.product_detail,
                      meta={'asin': asin, 'sale_rank': sale_rank, **response.meta})

    def product_detail(self, response):
        data = self.response_json(response)
        a =1

    def read_input_file(self):
        file_path = os.path.join('input', 'Flaconi Sample2.csv')
        data = []

        try:
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    ean = row.get('EAN', '')
                    price = row.get('Price', '')
                    data.append({'EAN': ean, 'Price': price})
            return data
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return []
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def response_json(self, response):
        try:
            json_data = json.loads(response.text) or {}
        except json.JSONDecodeError as e:
            print("Error decoding JSON: ", e)
            json_data = {}

        return json_data

    def form_data(self, asin):
        params = {
            'countryCode': 'DE',
            'locale': 'de-EN',
        }

        json_data = {
            'countryCode': 'DE',
            'itemInfo': {
                'asin': asin,
                'glProductGroupName': 'gl_beauty',
                'packageLength': '0',
                'packageWidth': '0',
                # 'packageHeight': '0',
                # 'dimensionUnit': '',
                # 'packageWeight': '0',
                # 'weightUnit': '',
                # 'afnPriceStr': '20.97',
                # 'mfnPriceStr': '20.97',
                'mfnShippingPriceStr': '0',
                'currency': 'EUR',
                'isNewDefined': False,
            },
            'programIdList': [
                'Core',
                'MFN',
            ],
        }

        body = {
            'params': json.dumps(params),
            'json_data': json.dumps(json_data),
        }

        return json_data

    def closed(self, reason):
        print('Total requests made in next_page:', self.counter)
