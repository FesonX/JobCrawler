# -*- coding: utf-8 -*-

import codecs
import csv
import re
import sys
import datetime

import pandas
import pymysql
import pymongo
from scrapy.exceptions import DropItem
from scrapy.conf import settings

'''
注释部分为以前写的Python2代码
'''
# reload(sys)
# sys.setdefaultencoding('utf8')

# class JobInfoPipeline(object):
    

#     def process_item(self, item, spider):
#         postItem = dict(item)
#         self.coll.insert(postItem)
#         return item

class jobCrawlerPipeline(object):
    """
    use for connecting to mongodb
    """
    def __init__(self):
        # connect to db
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # ADD if NEED account and password
        # self.client.admin.authenticate(host=settings['MONGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]


    """
    spider pipeline
    """

    def cut_word(self, word, method):
        """
        data standardization
        add bottom_salary field
        add top_salary field
        """
        if method == 'bottom':
            length = len(word)
            if (word.find('万') == -1):
                if (word.find('以下') != -1):
                    # XX千以下
                    postion = word.find('以下')
                    # salary_min = str(word[:(postion - 5)])
                    salary_min = (word[:(postion - 1)])
                elif (word.find('以上') != -1):
                    postion = word.find('以上')
                    # salary_min = str(float(word[:postion - 5]))
                    salary_min = (float(word[:postion - 1]))
                else:
                    # XX千/月
                    postion = word.find('-')
                    salary_min = (float(word[:(postion)]))
            else:
                if (word.find('年') == -1):
                    if (word.find('以下') != -1):
                        # XX万以下
                        postion = word.find('以下')
                        # salary_min = str(float(word[:(postion - 5)]) * 10)
                        salary_min = (float(word[:(postion - 1)]) * 10)
                    elif (word.find('以上') != -1):
                        # XX万以上
                        postion = word.find('以上')
                        # salary_min = str(float(word[:postion - 5]) * 10)
                        salary_min = (float(word[:postion - 1]) * 10)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        salary_min = (float(word[:(postion)]) * 10)
                    else:
                        # XX万/月
                        postion = word.find('-')
                        salary_min = (float(word[:(postion)]) * 10)

                else:
                    if (word.find('以下') != -1):
                        # XX万以下/年
                        postion = word.find('以下')
                        salary_min = (float(word[:(postion - 1)]) / 1.2)
                    elif (word.find('以上') != -1):
                        postion = word.find('以上')
                        salary_min = (float(word[:postion - 1]) / 1.2)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        salary_min = (float(word[:(postion)]) / 1.2)
                    else:
                        # XX万/年
                        postion = word.find('-')
                        salary_min = word[:(postion)]
                        salary_min = (float(salary_min) / 1.2)
            return salary_min

        if method == 'top':
            length = len(word)
            if (word.find('万') == -1):
                if (word.find('以下') != -1):
                    # XX千以下
                    postion = word.find('以下')
                    # salary_max = str(float(word[:(postion - 5)]))
                    salary_max = (float(word[:(postion - 1)]))
                elif (word.find('以上') != -1):
                    postion = word.find('以上')
                    # salary_max = str(float(word[:postion - 5]))
                    salary_max = (float(word[:(postion - 1)]))
                else:
                    # XX千/月
                    postion = word.find('-')
                    # salary_max = str(float(word[(postion + 1):(length - 11)]))
                    salary_max = word[postion + 1:(len(word) - 3)]
            else:
                if (word.find('年') == -1):
                    if (word.find('以下') != -1):
                        # XX万以下
                        postion = word.find('以下')
                        # salary_max = str(float(word[:(postion - 5)]) * 10)
                        salary_max = (float(word[:(postion - 1)]) * 10)
                    elif (word.find('以上') != -1):
                        # XX万以上
                        postion = word.find('以上')
                        # salary_max = str(float(word[:postion - 5]) * 10)
                        salary_max = (float(word[:(postion - 1)]) * 10)
                    else:
                        # XX万/月
                        postion = word.find('-')
                        # salary_max = str(float(word[(postion + 1):(length - 11)]) * 10)
                        salary_max = (float(word[postion + 1:(len(word) - 3)]) * 10)

                else:
                    if (word.find('以下') != -1):
                        # XX万以下/年
                        postion = word.find('以下')
                        # salary_max = str(float(word[:(postion - 5)]) / 1.2)
                        salary_max = (float(word[:(postion - 1)]) / 1.2)
                    elif (word.find('以上') != -1):
                        # XX万以上一年
                        postion = word.find('以上')
                        # salary_max = str(float(word[:postion - 5]) / 1.2)
                        salary_max = (float(word[:(postion - 1)]) / 1.2)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        salary_max = (float(word[:(postion)]) / 1.2)
                    else:
                        # XX万/年
                        postion = word.find('-')
                        # salary_max = word[(postion + 1):(length - 11)]
                        salary_max = word[(postion + 1):(len(word) - 3)]
                        salary_max = (int(salary_max) / 1.2)
            return salary_max

    def open_spider(self, spider):
        # """
        # called when open the spider
        # you can create database connection here
        # """
        pass

    def close_spider(self, spider):
        # """
        # called when close the spider
        # """
        pass


    def process_item(self, item, spider):
        if spider.name == 'jobCrawler':
            # Get data from item
            job_name = item['job_name']
            salary = item['salary']

            dirty_job_name = re.compile(r'(\*|在家|试用|体验|无需|无须|试玩|红包)+')
            dirty_salary = re.compile(r'(小时|天)+')

            # clean dirty data
            if(dirty_job_name.search(str(job_name))):
                raise DropItem("Dirty data %s" % item)
            if(dirty_salary.search(str(salary))):
                raise DropItem("Dirty data %s" % item)
            if(salary is None):
                raise DropItem("Dirty data %s" % item)

            # sort out data

            # 添加51Job缺失的年份,在跨年份的爬取可能会出错
            day = ''.join(item['create_time'])
            day = datetime.datetime.strptime(day, '%m-%d')
            day = day.replace(datetime.date.today().year) 
            item['create_time'] = day

            salary = ''.join(salary)

            item['salary_min'] = float(self.cut_word(salary, method='bottom'))
            item['salary_max'] = float(self.cut_word(salary, method='top'))
            # To Reduce Compute Time in Django, let Scrapy Pipeline compute average salary
            item['salary_avg'] = round((item['salary_max'] + item['salary_min'] / 2), 2)
        if spider.name == 'entrance':
            key_word = item['key_word']

            dirty_key_word = re.compile(r'(其它)+')

            if(dirty_key_word.search(str(key_word))):
                raise DropItem("Dirty data %s" % item)

        postItem = dict(item)
        self.coll.insert(postItem)

        return item
