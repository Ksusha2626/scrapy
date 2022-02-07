import scrapy
from jobparser.items import JobparserItem
from scrapy.http import HtmlResponse


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/qa-engineer.html']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[contains(@class,'dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            "//div[contains(@class,'vacancy-item')]//a[contains(@target,'_blank')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath('//div[contains(@class, "vacancy-base-info")]/*/*//h1/../span/span/text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
