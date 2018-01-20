# -*- coding: utf-8 -*-
import scrapy
import re
import chardet
from scrapy.contrib.spiders import CrawlSpider
from httplib2 import Response, has_timeout
from dlut.items import DlutItem

class DultSpider(CrawlSpider):
    name = 'dlut'
    start_urls = ['http://news.dlut.edu.cn/']
    
    def __init__(self):
        self.module = []
        self.modules = []
        self.article_lists = []
    def parse(self,response):
        all_module_names = []
        all_url_lists = []
        
        for n in range(7):
            module = response.xpath('//div[@class = "top"]/text()').extract()[n]
            all_module_names.append(module)
            lists_url = response.xpath('//div[@class = "top"]/span/a/@href').extract()[n]
            all_url_lists.append(lists_url)
        
        module = response.xpath('//div[@class = "title"]/text()').extract()[1]
        all_module_names.append(module)
        lists_url = response.xpath('//div[@class = "title"]/span/a/@href').extract()[0]
        all_url_lists.append(lists_url)
        
        for n in range(4):    
            module = response.xpath('//div[@class = "title"]/text()').extract()[4+n]
            all_module_names.append(module)
            lists_url = response.xpath('//div[@class = "title"]/span/a/@href').extract()[n+1]
            all_url_lists.append(lists_url)
            
        module = response.xpath('//div[@style="float:left;"]/text()').extract()[0]
        all_module_names.append(module)
        lists_url = response.xpath('//span[@style="float:right;"]/a/@href').extract()[0]
        all_url_lists.append(lists_url)
        
        module = response.xpath('//div[@class = "top"]/text()').extract()[7]
        all_module_names.append(module)
        all_module_names.append(module)
        lists_url = "http://news.dlut.edu.cn/article/tongzhi/1.shtml"
        all_url_lists.append(lists_url)
        lists_url = "http://news.dlut.edu.cn/article/jiangzuo/1.shtml"
        all_url_lists.append(lists_url)
        
        for n in range(len(all_module_names)):
            #print all_url_lists[n]
            yield scrapy.FormRequest(all_url_lists[n],meta = {'module':all_module_names[n]},callback = self.urllist_parse)
        
    def urllist_parse(self,response):
        module = response.meta['module']
        for n in range(5):
            new_url_list = response.url[:-7] + str(n+1) + response.url[-6:]
            yield scrapy.FormRequest(new_url_list,callback = self.url_parse,meta = {'module':module})
            
    def url_parse(self,response):
        module = response.meta['module']
        urls = response.xpath('//ul[@class="mode-txtlink c-lists"]/li/a/@href').extract()
        for url in urls:
            m = re.search(r'http://news.dlut.edu.cn/article/\w{4,}/.*',url)
            if m:
                yield scrapy.FormRequest(url,callback = self.article_parse,meta = {'module':module})
            
    def article_parse(self,response):
        item = DlutItem()
        author = ''
        click  = ''
        resource = ''
        module = response.meta['module']
        id = response.url
        title    = response.xpath('//h1[@style="text-align:center;"]/text()').extract()

        all_mes  = response.xpath('//div[@class="arti-atttibute"]/span/text()').extract()
        all_mes2 = ','.join(response.xpath('//div[@class="arti-atttibute"]/text()').extract())
        if re.search(ur'\u65f6\u95f4',all_mes2):
            has_time = 1
        else:
            has_time = 0
        
        if re.search(ur'\u70b9\u51fb',all_mes2):
            has_click = 1
        else:
            has_click = 0
            
        for n in all_mes:
            
            if has_click:
                a=re.findall(ur'\d{1,}',n)
                if a:
                    if a[0] == n:
                        click = n
                        has_click = 0
                    elif a[0] != n:
                        click = ''
            if has_time:
                if re.match(ur'\d{4}-\d{2}',n):
                    time = n
            if re.search(ur'\u4f5c\u8005',n):
                author = n
            if re.search(ur'\u6765\u6e90',n):
                resource = n
        content = response.xpath('//div[@id="ctrlfscont"]/p/text()').extract()
        item['id'] = id
        item['title'] = title
        item['author'] = author
        item['resource'] = resource
        item['time'] = time
        item['click'] = click
        item['module'] = module
        item['content'] = content
#         print item['id'],item['title'],item['author'],item['resource'],item['time'],item['click'],item['module'] ,item['content']
        return item

    