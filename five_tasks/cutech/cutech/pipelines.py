# -*- coding: utf-8 -*-
import MySQLdb.cursors
import scrapy
from scrapy.contrib import spiderstate
from scrapy.contrib.pipeline.images import ImagesPipeline
import subprocess
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import settings

class CutechPipelines(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool(dbapiName='MySQLdb',
            host='localhost',
            db='cutech',
            user='root',
            passwd='ybj',
            cursorclass= MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
            )
	def process_item(self,items,spider):
		self.dbpool.runInteraction(self._conditional_insert,items)
		return items   
        	
	def _conditional_insert(self,tx,items):  
#         raw_input('input:____________________________________')
        # sql = 'insert into news(title , poster_name , post_time , content) values (%s,%s,%s,%s)'
		sql = r'insert into news(title , poster_name , post_time , content , module,url) values (%s,%s,%s,%s,%s,%s)'
		param = (items['title'], items['poster_name'], items['post_time'] ,items['content'],items['module'],items['url']) 
		tx.execute(sql,param) 
