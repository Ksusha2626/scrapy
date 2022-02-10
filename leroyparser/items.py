# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def parse_number(value: str):
    value = value.strip().replace(' ', '')
    try:
        if value.isnumeric():
            value = int(value)
        else:
            value = float(value)
    except Exception as e:
        print(e)
    return value


class LeroyparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(parse_number),
                         output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())

