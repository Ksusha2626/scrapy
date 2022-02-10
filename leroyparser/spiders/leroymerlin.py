import scrapy
from leroyparser.items import LeroyparserItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, category, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{category}']

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath('//div[contains(@class, "largeCard")]/a['
                               '@data-qa="product-name"]/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    @staticmethod
    def parse_ads(response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('photos', '//img[@alt="product image"]/@src')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_value('url', response.url)
        yield loader.load_item()
