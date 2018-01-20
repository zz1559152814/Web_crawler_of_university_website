# -*- coding: utf-8 -*-  
import scrapy
from scrapy import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from meituan.items import Movie_mes,Cinema_mes,City_mes,City_mes

# class herfLinkExtractor(LinkExtractor):
# 		allow = r'http://[a-z]{1,}.meituan.com/dianying/*'

class MovieSpider(CrawlSpider):
	name = 'meituan'
	start_urls = ['http://www.meituan.com/index/changecity/initiative']
	allow_domains = ['meituan.com']
	
	#deal with the home of all cities    
	#[http://www.meituan.com/index/changecity/initiative]
	def parse(self,response):
		sel = scrapy.Selector()	
		citys = []
		city_name = response.xpath("//div[@class]/ol/li/p/span/a/text()").extract()
		city_url = response.xpath("//div[@class]/ol/li/p/span/a/@href").extract()

		for n in range(len(city_name)):
			city_mes = City_mes()
			city_mes['city_name'] = city_name[n]
			print city_mes['city_name'] 
			# citys.append(city_mes)
			yield city_mes
			