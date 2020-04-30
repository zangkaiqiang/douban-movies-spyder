# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from  douban.database import engine
import pandas as pd

class DoubanPipeline(object):
    def process_item(self, item, spider):
        self.save_item(item)
        return item

    def save_item(self,item):
        df = pd.DataFrame(dict(item), index=[0])
        df.to_sql('movies',engine,if_exists='append',index=False)

class MoviePipeline(object):
    def process_item(self, item, spider):

        return item

