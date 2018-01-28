# -*- coding: utf-8 -*-

import codecs
import csv
import re
import sys

import pandas
import pymysql
from scrapy.exceptions import DropItem

'''
注释部分为以前写的Python2代码
'''
# reload(sys)
# sys.setdefaultencoding('utf8')

class jobCrawlerPipeline(object):
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
                    salary_min = str(word[:(postion - 1)])
                elif (word.find('以上') != -1):
                    postion = word.find('以上')
                    # salary_min = str(float(word[:postion - 5]))
                    salary_min = str(float(word[:postion - 1]))
                else:
                    # XX千/月
                    postion = word.find('-')
                    salary_min = str(float(word[:(postion)]))
            else:
                if (word.find('年') == -1):
                    if (word.find('以下') != -1):
                        # XX万以下
                        postion = word.find('以下')
                        # salary_min = str(float(word[:(postion - 5)]) * 10)
                        salary_min = str(float(word[:(postion - 1)]) * 10)
                    elif (word.find('以上') != -1):
                        # XX万以上
                        postion = word.find('以上')
                        # salary_min = str(float(word[:postion - 5]) * 10)
                        salary_min = str(float(word[:postion - 1]) * 10)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        salary_min = str(float(word[:(postion)]) * 10)
                    else:
                        # XX万/月
                        postion = word.find('-')
                        salary_min = str(float(word[:(postion)]) * 10)

                else:
                    if (word.find('以下') != -1):
                        # XX万以下/年
                        postion = word.find('以下')
                        salary_min = str(float(word[:(postion - 1)]) / 1.2)
                    elif (word.find('以上') != -1):
                        postion = word.find('以上')
                        salary_min = str(float(word[:postion - 1]) / 1.2)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        salary_min = str(float(word[:(postion)]) / 1.2)
                    else:
                        # XX万/年
                        postion = word.find('-')
                        salary_min = word[:(postion)]
                        salary_min = str(float(salary_min) / 1.2)
            return salary_min

        if method == 'top':
            length = len(word)
            if (word.find('万') == -1):
                if (word.find('以下') != -1):
                    # XX千以下
                    postion = word.find('以下')
                    # salary_max = str(float(word[:(postion - 5)]))
                    salary_max = str(float(word[:(postion - 1)]))
                elif (word.find('以上') != -1):
                    postion = word.find('以上')
                    # salary_max = str(float(word[:postion - 5]))
                    salary_max = str(float(word[:(postion - 1)]))
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
                        salary_max = str(float(word[:(postion - 1)]) * 10)
                    elif (word.find('以上') != -1):
                        # XX万以上
                        postion = word.find('以上')
                        # salary_max = str(float(word[:postion - 5]) * 10)
                        salary_max = str(float(word[:(postion - 1)]) * 10)
                    else:
                        # XX万/月
                        postion = word.find('-')
                        # salary_max = str(float(word[(postion + 1):(length - 11)]) * 10)
                        salary_max = str(float(word[postion + 1:(len(word) - 3)]) * 10)

                else:
                    if (word.find('以下') != -1):
                        # XX万以下/年
                        postion = word.find('以下')
                        # salary_max = str(float(word[:(postion - 5)]) / 1.2)
                        salary_max = str(float(word[:(postion - 1)]) / 1.2)
                    elif (word.find('以上') != -1):
                        # XX万以上一年
                        postion = word.find('以上')
                        # salary_max = str(float(word[:postion - 5]) / 1.2)
                        salary_max = str(float(word[:(postion - 1)]) / 1.2)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        salary_max = str(float(word[:(postion)]) / 1.2)
                    else:
                        # XX万/年
                        postion = word.find('-')
                        # salary_max = word[(postion + 1):(length - 11)]
                        salary_max = word[(postion + 1):(len(word) - 3)]
                        salary_max = str(int(salary_max) / 1.2)
            return salary_max

    def open_spider(self, spider):
        # """
        # called when open the spider
        # create database connection
        # """
        # self.conn = pymysql.connect(
        #     host='localhost',
        #     user='root',
        #     passwd='mysql',
        #     db='scrapyDB',
        #     charset='utf8',
        #     cursorclass=pymysql.cursors.DictCursor)
        pass

    def close_spider(self, spider):
        # """
        # called when close the spider
        # open the csv and then insert data into database
        # """
        # try:
        #     # open the cursor
        #     self.cursor = self.conn.cursor()

        #     # get data from csv file
        #     # reload data
        #     f = open(r'job.csv', 'r')
        #     f.close()
        #     job_info = pandas.read_csv(r'job.csv', iterator=True,chunksize=1,
        #                                header=None,names=
        #                                ['job_id','job_name','company','address','bottom_salary','top_salary','salary','time'])

        #     # store data
        #     for i, job in enumerate (job_info):
        #         # use -1 or ' ' to fill NAN
        #         job = job.fillna({'job_name':'','company':'','address':'','time':''})
        #         job = job.fillna(-1)
        #         # transform series to list type
        #         job = job.values[0]

        #         sql = 'INSERT INTO tb_job(job_id,job_name,company,address,bottom_salary,top_salary,salary,time)' \
        #               'VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
        #               job[1], job[7], job[3], job[5], job[2], job[6], job[0], job[4])
        #         self.cursor.execute(sql)
        #     self.conn.commit()

        # finally:
        #     # close the connection
        #     self.conn.close()
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
            salary = ''.join(salary)
            item['salary_min'] = self.cut_word(salary, method='bottom')
            item['salary_max'] = self.cut_word(salary, method='top')
        if spider.name == 'entrance':
            key_word = item['key_word']

            dirty_key_word = re.compile(r'(其它)+')

            if(dirty_key_word.search(str(key_word))):
                raise DropItem("Dirty data %s" % item)

        return item
