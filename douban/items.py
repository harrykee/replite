# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ISBN =scrapy.Field()
    title =scrapy.Field()
    rate = scrapy.Field()
    author = scrapy.Field()
    score = scrapy.Field()
    press =scrapy.Field()
    pretime = scrapy.Field()
    prise =scrapy.Field()
    number=scrapy.Field()

