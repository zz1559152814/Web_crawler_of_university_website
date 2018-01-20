# -*- coding: utf-8 -*-
import MySQLdb.cursors
import scrapy
from scrapy.contrib import spiderstate
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import settings

class DlutPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(dbapiName='MySQLdb',
            host='localhost',
            db='dlut',
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
        sql = r'insert into news(id ,title ,time ,author ,resource ,click,module,content) values (%s,%s,%s,%s,%s,%s,%s,%s)'
        #param = ('asd','dsf','zxc','qwe','fsfsd','sadfsa','xvczxvcxz','vdasrSDF')
#         print items['time'],items['author'],items['resource'],items['click'],items['module'],items['content']
        param = (items['id'], items['title'][0], items['time'] ,items['author'][0],items['resource'][0],items['click'][0],items['module'],items['content'][0])
        tx.execute(sql,param) 
