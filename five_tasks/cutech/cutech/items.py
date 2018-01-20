# -*- coding: utf-8 -*-

# Define here the modules for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CutechItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title       = scrapy.Field()
    poster_name = scrapy.Field()
    post_time   = scrapy.Field()
    content     = scrapy.Field()
    module      = scrapy.Field()
    url         = scrapy.Field()