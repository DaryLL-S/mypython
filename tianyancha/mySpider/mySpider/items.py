# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    companyName = scrapy.Field()
    tag = scrapy.Field()
    foundDate = scrapy.Field()
    pass
