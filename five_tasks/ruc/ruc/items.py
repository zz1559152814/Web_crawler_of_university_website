# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RucItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	id         = scrapy.Field()
	title      = scrapy.Field()
	time       = scrapy.Field()
	resource   = scrapy.Field()
	content    = scrapy.Field()
	module     = scrapy.Field()
	page_views = scrapy.Field()
