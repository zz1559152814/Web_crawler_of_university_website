import scrapy
from scrapy.contrib.spiders import CrawlSpider
class login(CrawlSpider):
	name = 'login'
	start_urls = ['https://accounts.douban.com/login']

	def __init__(self):
		self.form_email = '15319779873'
		self.form_password = 'an18392886383ybj'
		self.redir = 'http://www.douban.com'
	

	def start_requests(self):
		return [scrapy.FormRequest("https://accounts.douban.com/login",
    		formdata={'form_email':'15319779873',
    		'form_password':'an18392886383ybj',
    		'self.redir':'http://www.douban.com'},
    		callback=self.logged_in)]
	
	def logged_in(self, response):
		print response.xpath('//div[@class="nav-logo"]/a')
		return
	# def parse(self,response):
	# 	return scrapy.Request(
	# 			'https://accounts.douban.com/login',
	# 			callback=self.parse1,
	# 			meta = {'dont_redirect': True,
	# 			'handle_httpstatus_list': [302]},
	# 			'form_email'='15319779873',
	# 			'form_password'='an18392886383ybj',
	# 			'self.redir'='http://www.douban.com')
	# def parse1(self,response):
	# 	print response.body
	# 	return 
