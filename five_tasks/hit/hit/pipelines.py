# -*- coding: utf-8 -*-
import MySQLdb.cursors
import scrapy
from scrapy.contrib import spiderstate
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import settings

class HitPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(dbapiName='MySQLdb',
            host='localhost',
            db='hit',
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
        sql = r'insert into news(id ,title ,time ,resource ,click,module,content) values (%s,%s,%s,%s,%s,%s,%s)'
        #print items['time'],items['resource'],items['click'],items['module'],items['content']
        param = (items['id'], items['title'], items['time'] ,items['resource'],items['click'],items['module'],items['content'])
        tx.execute(sql,param) 
