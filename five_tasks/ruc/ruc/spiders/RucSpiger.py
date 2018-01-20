import scrapy
import re
import chardet
import os
import urllib2
import pp
from urllib2 import Request, urlopen, URLError, HTTPError
from multiprocessing import Process, Queue
from scrapy.contrib.spiders import CrawlSpider
from ruc.items import RucItem
import MySQLdb

q_camp = Queue()
q_important = Queue()
def judge_state(url):
	req = Request(url)
	try:
		response = urlopen(req)
		return 1
	except HTTPError, e:
		return 0
	except URLError, e:
		return -1

def camp_test():
	global q_camp
	camp_news_root = 'http://news.ruc.edu.cn/archives/category/camp_news/page/'
	num = 0
	state = 1
	num = 380
	while(state == 1):
		num = num + 1
		camp_news_url = camp_news_root + str(num)
# 		print camp_news_url
		state = judge_state(camp_news_url)
	camp_url_num = num - 1
	q_camp.put(camp_url_num)

def important_test():
	global q_important
	important_news_root = 'http://news.ruc.edu.cn/archives/category/important_news/page/'
	num = 0
	state = 1
	num = 310
	while(state == 1):
		num = num + 1
		important_news_url = important_news_root + str(num)
# 		print important_news_url
		state = judge_state(important_news_url)
	important_url_num = num - 1
	q_important.put(important_url_num)

class RucSpider(CrawlSpider):
	name = 'ruc'
	start_urls = ['http://news.ruc.edu.cn/archives/category/special_news']
	
	def __init__(self):
		global q_important
		global q_camp
		p1 = Process(target=camp_test)
		p2 = Process(target=important_test)
		p1.start()
		p2.start()
		p1.join()
		p2.join()
		self.important_url_num = q_important.get()
		self.camp_url_num = q_camp.get()
		print self.important_url_num, self.camp_url_num
		self.important_news_root = 'http://news.ruc.edu.cn/archives/category/important_news/page/'
		self.camp_news_root = 'http://news.ruc.edu.cn/archives/category/camp_news/page/'
		special_news_urls = []
		self.conn = MySQLdb.connect(host="localhost", user="root", passwd="ybj", db="ruc", charset="utf8")
		self.cursor = self.conn.cursor() 

		# print response.body
	def Request(self, url, callback, meta={}):
		# print 111111111111111111111111111111
		req = urllib2.Request(url)
		r = urllib2.urlopen(req)
		html = r.read()
		response = scrapy.http.Response(url)
		response._set_body = html
		print type(response)
		callback(response, meta)
		# print url
	
	def parse(self, response):
		global important_url_num
		global camp_url_num
		self.special_news_urls = response.xpath('//div[@class="content_col_2_list"]/ul/li/a/@href').extract()
		p1 = Process(target=self.camp_generator)
		p2 = Process(target=self.important_generator) 
		p3 = Process(target=self.special_generator)	
		p1.start()
		p2.start()
		p3.start()
		p1.join()
		p2.join()
		p3.join()

	def special(self):
		for url in self.special_news_urls:
			yield self.Request(str(url), self.articles_list,
				{'module':u'\u4e13\u9898\u65b0\u95fb'})
	def special_generator(self):
		special_func = self.special()
		for n in range(len(self.special_news_urls)):
			a = special_func.next()


	def important(self):
		for n in range(self.important_url_num):
			url = self.important_news_root + str(n + 1)
			# print url
			yield self.Request(str(url), self.articles_list,
				{'module':u'\u4eba\u5927\u8981\u95fb'})
	def important_generator(self):
		important_func = self.important()
		for n in range(self.important_url_num):
			important_func.next()

	def camp(self):
		for n in range(self.camp_url_num):
			url = self.camp_news_root + str(n + 1)
			# print url
			yield self.Request(str(url), self.articles_list,
				{'module':u'\u4eba\u5927\u8981\u95fb'})
	def camp_generator(self):
		camp_func = self.camp()
		for n in range(self.camp_url_num):
			camp_func.next()

	def articles_list(self, response, meta):
		# module = response.meta['module']
		# print response.xpath('//a[@class="rss"]/@href').extract()
		sel = scrapy.Selector(text=response._set_body)
		urls = sel.xpath('//div[@class="content_col_2_list"]/ul/li/a/@href').extract()
		for url in urls:
# 			print url
			return self.Request(str(url), callback=self.next_parse, meta=meta)

	def next_parse(self, response, meta):
		sel = scrapy.Selector(text=response._set_body)
		# title
		title = ','.join(sel.xpath('//div[@class="nc_title"]/text()').extract()).encode('utf8')
		# time 
		time = ','.join(sel.xpath('//div[@class="nc_meta"]/span/text()').extract())
		# resource
		resource = ','.join(sel.xpath('//div[@class="nc_author"]/text()').extract())
		# content
		all_content = []
		content_root = sel.xpath('//div[@class="nc_body"]/descendant::node()/text()').extract()
		for elem in content_root:
			if elem != '\r\n\t':
				all_content.append(elem)	
		content = '\n'.join(all_content).encode('utf8')
		# page view
		page_views = ','.join(sel.xpath('//div[@class="views"]/span/text()').extract())
		# module
		module = meta['module']
		mes = []
		mes.append(response.url)
		mes.append(title)
		mes.append(time)
		mes.append(resource)
		mes.append(content)
		mes.append(page_views)
		mes.append(module)
# 		print response.url
		self.Insert_into_db(mes)
	def Insert_into_db(self, *mes):
		sql = r'insert into news(id,title,time,resource,content,page_views,module) values (%s,%s,%s,%s,%s,%s,%s)'
		param = (mes[0][0], mes[0][1], mes[0][2], mes[0][3] , mes[0][4], mes[0][5], mes[0][6])
		self.cursor.execute(sql, param)
		self.conn.commit()

