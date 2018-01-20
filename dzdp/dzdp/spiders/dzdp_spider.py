# -*- coding: utf-8 -*-  
import scrapy
from scrapy import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from dzdp.items import Movie_mes,Cinema_mes,City_mes,City_mes

# class herfLinkExtractor(LinkExtractor):
# 		allow = r'http://[a-z]{1,}.meituan.com/dianying/*'

class MovieSpider(CrawlSpider):
	name = 'dzdp'
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

			citys.append(city_mes)
			yield scrapy.Request(
				city_url[n]+'/dianying/cinemalist',
				callback=self.city_cinema_parse1,
				meta = {'dont_redirect': True,'handle_httpstatus_list': [302]})

	#deal with the page full of cinema names  
	#[http://sh.meituan.com/dianying/cinemalist]
	def city_cinema_parse1(self,response):
		sel = scrapy.Selector()
		# citys = response.meta['citys']
		# response.xpath('//div[@class="paginator-wrapper"]/ul/li/a[@href="***"]/@href').extract()
		cinemalisturl = [response.url[:-20]+ url for url in response.xpath('//div[@class="paginator-wrapper"]/ul/li/a[@href]/@href').extract()]
		cinemalisturl.append(response.url)
		cinemalisturl = set(cinemalisturl)
		# return cinemalisturl
		for page in cinemalisturl:
			print page
			yield scrapy.Request(
				page,
				callback=self.city_cinema_parse2,
				meta = {'citys':citys})

	#get all the information of cinemas of last city
	#[http://sh.meituan.com/dianying/cinemalist/page-n]
	# def city_cinema_parse2(self,response):
	# 	citys      = response.meta['citys']
	# 	cinema_name    = response.xpath('//div[@class="J-cinema-item cinema-item cf"]/div/h4/a/text()').extract()
	# 	cinema_address = response.xpath('//div[@class="J-cinema-item cinema-item cf"]/div/dl/dd/text()').extract()
	# 	cinema_grade   = response.xpath('//div[@class="J-cinema-item cinema-item cf"]/div/h4/span/strong/text()').extract()
	# 	# cinema_city    = response.xpath('//h2/a/text()').extract()[0][:2]
	# 	cinema_url     = response.xpath('//div[@class="J-cinema-item cinema-item cf"]/div/h4/a/@href').extract()
	# 	for n in range(len(cinema_name)):
\	# 		cinema_mes = Cinema_mes()
	# 		cinema_mes['name']    = cinema_name[n]
	# 		cinema_mes[address] = cinema_address[n]
	# 		cinema_mes[grade]   = cinema_grade[n]
	# 		# cinema_mes[city]    = cinema_city
	# 		citys.cinema_list.append(cinema_mes)
	# 		# print citys
	# 		yield citys
	# 			# cinema_url[n],callback = self.cinema_movie_parse1,
	# 			# meta={'citys':citys})
'''
	#get in the page of cinemas,there are many movie's information ,and next get in each movie apge
	#[http://sh.meituan.com/shop/1547372]
	def cinema_movie_parse1(self,response):
		movie_city = response.meta['city']
		movie_cinema = response.meta['cinema']
		movie_url = response.xpath('//div/header/a/@href').extract()
		for movieurl in movie_url:
			yield scrapy.Request(
				movieurl,
				callback = self.cinema_movie_parse2,
				meta={'citys':citys})			

	#get in the movie page ,and collect the movie information
	#[http://wx.meituan.com/movie/78684]
	def cinema_movie_parse2(self,response):
		citys      = response.meta['citys']
		movie_name 		   = response.xpath('//div[@class="movie-info__name"]/h2/text()').extract()[0]
		movie_release_time = response.xpath('//section/dl/dd/text()').extract()[0]
		movie_type         = response.xpath('//section/dl/dd/text()').extract()[1]
		movie_version      = response.xpath('//section/dl/dd/text()').extract()[2]
		movie_area         = response.xpath('//section/dl/dd/text()').extract()[3]
		movie_time         = response.xpath('//section/dl/dd/text()').extract()[4]
		movie_diector      = response.xpath('//section/dl/dd/text()').extract()[5]
		movie_star         = response.xpath('//section/dl/dd/text()').extract()[6]
		movie_price        = scrapy.Field()
		movie_score        = response.xpath('//strong[@class="rates"]/text()').extract()[0]+response.xpath('//strong[@class="rates-point"]/text()').extract()[0]
		for n in range(len(movie_name)):
			movie_mes = Movie_mes()
			movie_mes[name] = movie_name
			movie_mes[name] = movie_release_time
			movie_mes[name] = movie_type
			movie_mes[name] = movie_version
			movie_mes[name] = movie_area
			movie_mes[name] = movie_time
			movie_mes[name] = movie_diector
			movie_mes[name] = movie_star
			movie_mes[name] = movie_price
			movie_mes[name] = movie_score
			citys.city_mes[-1].cineam_mes[-1].movie_mes.append(movie_mes)
		return citys

#question:
	# 1.can class movie inherited from class cinema inherited from class city
'''	