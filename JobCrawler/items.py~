# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Join, MapCompose


class JobcrawlerItem(scrapy.Item):
    # 职位名
    job_name = scrapy.Field()
    # 公司名
    company = scrapy.Field()
    # 工作地点
    address = scrapy.Field()
    # 工资
    salary = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
    

class JobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    review_in = MapCompose(lambda x: x.replace("\n", " "))
    review_out = Join()
