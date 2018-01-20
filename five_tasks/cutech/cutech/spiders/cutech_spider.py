# -*- coding: utf-8 -*-
import scrapy
import re
import chardet
from scrapy.contrib.spiders import CrawlSpider
from cutech.items import CutechItem
import MySQLdb

class cutech_spider(CrawlSpider):
	name = 'cutech'
	start_urls = ['http://www.cutech.edu.cn/cn/index.htm']
	
	def __init__(self):
		self.root = 'http://www.cutech.edu.cn'
		conn = MySQLdb.connect(host="localhost",user="root",passwd="ybj",db="cutech",charset="utf8")
		cursor = conn.cursor() 
		sql = "create table news(title varchar(50),post_time varchar(20),poster_name varchar(30),content varchar(5000),module varchar(10),url varchar(100))CHARSET=utf8"
		cursor.execute(sql) 

	#取各个板块的链接
	#http://www.cutech.edu.cn/cn/index.htm
	def parse(self,response):
		sel = scrapy.Selector()	
		url_lists=response.xpath('//img[re:test(@src,".*more")]/parent::a/@href').extract()
		for url_list in url_lists:
			# print 'first'
			# print ','.join(self.start_urls)[:24]+url_list
			yield scrapy.FormRequest(self.root+url_list,callback=self.pages_parse1)

	#列表状的文章列表和表格状
	#http://www.cutech.edu.cn/cn/qslt/A0108index_1.htm
	def pages_parse1(self,response):
		if (response.url.find('dxph') == -1) and (response.url.find('zcfg') == -1):
			print 'aaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
			num = ','.join(response.xpath('//td[@class="fyinfo"]/b/text()').extract())[8:]
			page_count = int(num)
			for page in range(page_count):
				page_str = 'index_'+str(page+1)
				page_real = response.url.replace('index_1',page_str)
				yield scrapy.FormRequest(page_real,callback=self.news_url_parse)
		else:
			print '111111111111111111111111111111111111111111111111111111111111111111111'
			yield scrapy.FormRequest(response.url,callback=self.pages_parse2)
	#在大学排行和政策规范两个专栏中，下级页面是方块状
	#http://www.cutech.edu.cn/cn/zcfg/A0102index_1.htm
	def pages_parse2(self,response):
		hrefs = response.xpath('//td[@width="55"]/a[@target="_self"]/@href').extract()
		for href in hrefs:
			yield scrapy.FormRequest(self.root+url_list,callback=self.pages_parse)				

	#取出每篇文章的链接
	#http://www.cutech.edu.cn/cn/rxcz/A0127index_1.htm	
	def news_url_parse(self,response):
		news_urls_list = response.xpath('//td[@width="590"]/a[@target="_blank"]/@href').extract()
		for new_url in news_urls_list:
			# print "third"
			yield scrapy.FormRequest(self.root+new_url,callback=self.news_parse)

	def news_parse(self,response):
		cutech_item = CutechItem()
		#get info
		post_time   = response.xpath('//table[@class="cinfo"]/descendant::td/text()').extract()[1][8:]
		time = int(post_time.replace('-',''))
			#get title
		title  = response.xpath('//table[@class="ctitle"]/descendant::td/text()').extract()[0].encode('utf8')[2:]
		cutech_item['title'] = title
		# print cutech_item['post_time']
		#fet time
		cutech_item['post_time'] = time
		#get name
		poster_name = response.xpath('//table[@class="cinfo"]/descendant::td/text()').extract()[0].encode('utf8')[12:]
		cutech_item['poster_name'] = poster_name
		# print poster_name,len(post_time)
		#get module
		module =  ','.join(response.xpath('//a[@class="channelLink"]/text()').extract())
		cutech_item['module'] = module
		#get content 
		all_content = []
		content_root = response.xpath('//table[@class="ctab"]/tbody/tr/td/descendant::node()/text()').extract()
		for elem in content_root:
			if elem != '\r\n\t':
				all_content.append(elem)	
		final_content = '\n'.join(all_content)
		cutech_item['content'] = final_content
		#get url 
		cutech_item['url'] = response.url
		return cutech_item
