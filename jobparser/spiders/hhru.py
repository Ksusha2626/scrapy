import scrapy
from jobparser.items import JobparserItem
from scrapy.http import HtmlResponse


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?area=1&experience=between1And3&text=Qa+engineer',
        'https://hh.ru/search/vacancy?area=2&experience=between1And3&text=Qa+engineer'
    ]

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            "//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
