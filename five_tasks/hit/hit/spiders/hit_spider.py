# -*- coding: utf-8 -*-
import scrapy
import re
import chardet
from scrapy.contrib.spiders import CrawlSpider
from hit.items import HitItem


class HitSpider(CrawlSpider):

	name = 'hit'
	start_urls = ['http://news.hit.edu.cn/']

	def __init__(self):
		pass
	def parse(self,response):
		module_url  = []
		module_name = []
	
	#学校要闻 综合新闻 人才培养 科研在线 服务管理 国际合作 校园文化 校友之苑 深度策划 时势关注 理论学习 他山之石
		#get url
		url_list = response.xpath('//ul[@class="wp-menu clearfix"]/li/a/@href').extract()[1:13]
		for url in url_list:
			real_url = response.url + url
			module_url.append(real_url)
		#get name
		name_list = response.xpath('//ul[@class="wp-menu clearfix"]/li/a/text()').extract()[1:13]
		for n in name_list:
			module_name.append(n)
	#热点专题
		#get url
		url_list_rmzt = response.xpath('//div[@class="more-link"]/a/@href').extract()[8]
		zdzt_url = response.url + url_list_rmzt
		#get name
		name_list2 = response.xpath('//span[@class="title-text"]/text()').extract()[5]
		module_name.append(name_list2)
	#parse
		all_urls = []

		for n in range(len(module_url)):
			for num in range(5):
				real_url = module_url[n][:-4] + str(num+1) + module_url[n][-4:]
				all_urls.append(real_url)
		all_urls.append(zdzt_url)
		

		for l in range(len(all_urls)):
			if l != len(all_urls)-1:
				yield scrapy.FormRequest(all_urls[l],
					meta = {'module':module_name[l/5]},
					callback = self.actlist_parse)
			else:
				yield scrapy.FormRequest(all_urls[l],
					meta = {'module':module_name[l/5]},
					callback = self.rmzt_parse)

#######################
#######################
#######################			
#######################
#for topic expect rdzt#
	#http://news.hit.edu.cn/12ddh/98/ab/c3305a104619/page.htm
	def actlist_parse(self,response):
		module = response.meta['module']
		article_lists =  response.xpath('//span[@class="Article_Title Article_Title1"]/a/@href').extract()		
		for url in article_lists:
			real_url = 'http://news.hit.edu.cn/'+url
			print real_url
			yield scrapy.FormRequest(real_url,
				meta = {'module':module},
				callback = self.acticle_parse)		
	
	def acticle_parse(self,response):
		print 111111111111111111111111111111111111
		item = HitItem()
		#id 
		id = response.url
		#module 
		module = response.meta['module']
		#title
		title = response.xpath('//h1[@class="arti_title"]/text()').extract()[0]
		#time
		time = response.xpath('//p[@class="arti_metas"]/span[@class="arti_update"]/text()').extract()
		time = re.sub(ur'[\u4e00-\u9fa5]', '-',time[0])[:10]
		#content 
		content = ','.join(response.xpath('//div[@class="wp_articlecontent"]/descendant::text()').extract())
		#resource 
		some = response.xpath('//p[@class="arti_metas"]/span[@class="arti_from"]/a/text()').extract()
		if len(some) == 1:
			resource = some[0]
		else:
			resource = ''
			temp_index = 0
			if len(content) != 0:
				temp = content[temp_index]
				while(re.search(ur'[\u4e00-\u9fa5]',temp) is None):
					temp_index = temp_index + 1
					temp = content[temp_index]
				if len(temp) > 10:
					length = 10
				else:
					length = len(temp) 
				for n in range(length):
					if temp[n] == u'\uff08':
						resource = temp[:n]
			else:
				resource = None
		#click 
		click = response.xpath('//p[@class="arti_metas"]/span[@class="arti_views"]/span/text()').extract()[0]
		item['id'] = id
		item['module'] = module
		item['title'] = title
		item['time'] = time
		item['resource'] = resource
		item['click'] = click
		item['content'] = content
		return item

#######################
#######################
#######################			
#######################
#for topic rdzt#	
	#http://news.hit.edu.cn//91/list.htm
	def rmzt_parse(self,response):
		module = response.meta['module']		
		url_list = response.xpath('//span[@class="Article_Title Article_Title1"]/a/@href').extract()
		for topic in url_list:
			yield scrapy.FormRequest(topic,
					meta = {'module':module},
					callback = self.rmzt2_parse)	

	#http://news.hit.edu.cn/12ddh/
	def rmzt2_parse(self,response):
		module = response.meta['module']		
		w21_more = response.xpath('//a[@class="w21_more"]/@href').extract()
		more = response.xpath('//div[@class="more"]/a[@target]/@href').extract()
		if len(w21_more) == 1:
			artlist = 'http://news.hit.edu.cn'+	w21_more[0]
			yield scrapy.FormRequest(artlist,
				meta = {'module':module,'more':'w21_more'},
				callback = self.rmzt3_parse)	
		# elif len(more) == 1:
		# 	artlist = 'http://news01.hit.edu.cn'+ more[0]
		# 	print artlist
		# 	yield scrapy.FormRequest(artlist,
		# 		meta = {'module':module,'more':'more'},
		# 		callback = self.rmzt3_parse)	
	
	#http://news.hit.edu.cn/12ddh/1687/list.htm
	#http://news01.hit.edu.cn/specialAllArticles/103_1_0.htm
	def rmzt3_parse(self,response):
		more = response.meta['more']		
		module = response.meta['module']		
		article_lists = []
		if more == 'w21_more':
			urls = response.xpath('//span[@class="Article_Title"]/a/@href').extract()
			for url in urls:
				url = 'http://news.hit.edu.cn/' + url
				yield scrapy.FormRequest(url,
					meta = {'module':module},
					callback = self.article_w21_parse)	

	def article_w21_parse(self,response):
		item = HitItem()
		#id 
		id = response.url
		#module 
		module = response.meta['module']
		#title
		title = response.xpath('//h1[@class="arti_title"]/text()').extract()[0]
		#time
		time = response.xpath('//p[@class="arti_metas"]/span[@class="arti_update"]/text()').extract()[0][-10:]
		#resource 
		some = response.xpath('//p[@class="arti_metas"]/span[@class="arti_publisher"]/text()').extract()
		if len(some) == 1:
			resource = some[0][-3:]
		else:
			resource = None
		#click 
		click = response.xpath('//p[@class="arti_metas"]/span[@class="arti_views"]/span/text()').extract()[0]
		#content 
		content = ','.join(response.xpath('//div[@class="read"]/descendant::text()').extract())
		item['id'] = id
		item['module'] = module
		item['title'] = title
		item['time'] = time
		item['resource'] = resource
		item['click'] = click
		item['content'] = content
		return item

