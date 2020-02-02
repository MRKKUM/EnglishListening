# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import psycopg2
import pymongo

class KekePipeline(object):
    id = 0
    def __init__(self):

        host = '127.0.0.1'
        port = 27017
        db_name = '201802final'
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db['data_link']

    # 捕捉到item的时候执行
    def process_item(self, item,spider):
        book_info = dict(item)
        self.post.insert(book_info)
        return item



