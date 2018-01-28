# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Join, MapCompose


class JobcrawlerItem(scrapy.Item):
    # 职位ID
    job_id = scrapy.Field()
    # 职位名
    job_name = scrapy.Field()
    # 公司名
    company = scrapy.Field()
    # 工作地点
    job_city = scrapy.Field()
    # 工资
    salary = scrapy.Field()
    # 发布时间
    create_time = scrapy.Field()
    # 底薪
    salary_min = scrapy.Field()
    # 最高薪资
    salary_max = scrapy.Field()
    # 为了便于分类, 引入搜索关键词
    key_word = scrapy.Field()
    

class JobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    review_in = MapCompose(lambda x: x.replace("\n", " "))
    review_out = Join()

class EntranceItem(scrapy.Item):
    # 搜索关键词
    key_word = scrapy.Field()
    # 所属领域
    key_field = scrapy.Field()