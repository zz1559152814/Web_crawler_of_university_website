# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class City_mes(scrapy.Item):
	city_name = scrapy.Field()
	cinema_list = []

class Cinema_mes(scrapy.Item):
	name = scrapy.Field()
	address = scrapy.Field()
	grade = scrapy.Field()
	movie_list = []

class Movie_mes(scrapy.Item):
	name         = scrapy.Field()
	release_time = scrapy.Field()
	type         = scrapy.Field()
	version      = scrapy.Field()
	area         = scrapy.Field()
	time         = scrapy.Field()
	diector      = scrapy.Field()
	star         = scrapy.Field()
	price        = scrapy.Field()
	score        = scrapy.Field()

