# coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#realse memory of list
# import gc
# del listname
import json

class MeituanPipeline(object):

    def __init__(self):
        self.file = open('items.txt', 'w')

    def process_item(self, city_mes, spider):
        
    	#self.file.write(line)
        self.file.write(city_mes['city_name'].encode('utf8'))
        return city_mes
