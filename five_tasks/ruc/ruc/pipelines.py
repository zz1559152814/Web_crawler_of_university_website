# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb.cursors
import scrapy
from scrapy.contrib import spiderstate
from scrapy.contrib.pipeline.images import ImagesPipeline
import subprocess
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import settings


class RucPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool(dbapiName='MySQLdb',
            host='localhost',
            db='ruc',
            user='root',
            passwd='ybj',
            cursorclass= MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
            )
	def process_item(self,items,spider):
		self.dbpool.runInteraction(self._conditional_insert,items)    
        # print 111111111111111
		return items   
        	
	def _conditional_insert(self,tx,items):  
#         raw_input('input:____________________________________')
        # sql = 'insert into news(title , poster_name , post_time , content) values (%s,%s,%s,%s)'
		sql = r'insert into news(title , resource , content , page_views , module) values (%s,%s,%s,%s,%s)'
		param = (items['title'], items['resource'], items['content'] ,items['page_views'],items['module'])
		tx.execute(sql,param) 

