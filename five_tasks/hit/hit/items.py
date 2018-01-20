# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HitItem(scrapy.Item):
	id = scrapy.Field()
	module = scrapy.Field()
	title = scrapy.Field()
	time = scrapy.Field()
	resource = scrapy.Field()
	click = scrapy.Field()
	content = scrapy.Field()
