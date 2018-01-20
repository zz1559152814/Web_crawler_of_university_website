# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HustItem(scrapy.Item):
	id       = scrapy.Field()
	title    = scrapy.Field()
	time     = scrapy.Field()
	module   = scrapy.Field()
	#about 
	resource   = scrapy.Field()
	click      = scrapy.Field()
	author     = scrapy.Field()
	content    = scrapy.Field()