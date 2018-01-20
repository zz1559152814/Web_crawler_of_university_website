# -*- coding: utf-8 -*-
import scrapy
import re
import chardet
from scrapy.contrib.spiders import CrawlSpider
from hust.items import HustItem


class HustSpider(CrawlSpider):

	name = 'hust'
	start_urls = ['http://news.hustonline.net/']

	def parse(self,response):
		module_names = response.xpath('//ul[@class="nav"]/li/a/text()').extract()[1:4]
		module_urls = response.xpath('//ul[@class="nav"]/li/a/@href').extract()[1:4]
		for n in range(3):
			module_urls.append(response.xpath('//ul[@class="nav"]/li/a/@href').extract()[5+n])
			module_names.append(response.xpath('//ul[@class="nav"]/li/a/text()').extract()[5+n])
		for n in range(6):
			module_urls.append(response.xpath('//ul[@class="nav"]/li/a/@href').extract()[9+n])
			module_names.append(response.xpath('//ul[@class="nav"]/li/a/text()').extract()[9+n])

		for n in range(len(module_urls)):
			root_url = 'http://news.hustonline.net' + module_urls[n] 
			for n in range(5):
				real_url = root_url + '?page' + str(n)
				yield scrapy.FormRequest(real_url,
					meta = {'module':module_names[n]},
					callback = self.actlist_parse)

	def actlist_parse(self,response):
		module = response.meta['module'].encode('utf8')
		article_urls = response.xpath('//ul[@class="newsList"]/li/span/preceding-sibling::a/@href').extract()
		article_names = response.xpath('//ul[@class="newsList"]/li/span/preceding-sibling::a/text()').extract()
		article_times = response.xpath('//ul[@class="newsList"]/li/span/text()').extract()
		for n in range(len(article_urls)):
			yield scrapy.FormRequest(article_urls[n],
					meta = {'module':module,'article_name':article_names[n],
					'article_time':article_times[n]},
					callback = self.article_parse)
	
	def article_parse(self,response):
		item = HustItem()

		id = response.url
		title = response.meta['article_name']
		time  = response.meta['article_time']
		module = response.meta['module']
		#about 
		about_root = response.xpath('//p[@class="about"]/span/text()').extract()
		if len(about_root) != 0:
			resource = about_root[0][3:]
			click    = about_root[1][5:-1]
			author   = about_root[3][3:]
		else:
			resource = None
			click    = None
			author   = None

		# print u'这是一个about'.encode('utf8')
		# print response.url
		# for m in about_root:
		# 	print m.encode('utf8')
		# print '\n\n\n\n\n\n\n'
		#content 
		content =  ','.join(response.xpath('//div[@class="article"]/descendant::text()').extract())
		
		item['id'] = id
		item['module'] = module
		item['title'] = title
		item['time'] = time
		item['author'] = author
		item['resource'] = resource
		item['click'] = click
		item['content'] = content
		return item
