# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re
from scrapy.exceptions import DropItem
import sys
import csv
import codecs
import pandas

reload(sys)
sys.setdefaultencoding('utf8')


class jobCrawlerPipeline(object):

    def cut_word(self, word, method):
        if method == 'bottom':
            length = len(word)
            if (word.find('万') == -1):
                if (word.find('以下') != -1):
                    # XX千以下
                    postion = word.find('以下')
                    bottomSalary = str(word[:(postion - 5)])
                elif (word.find('以上') != -1):
                    postion = word.find('以上')
                    bottomSalary = str(float(word[:postion - 5]))
                else:
                    # XX千/月
                    postion = word.find('-')
                    bottomSalary = str(float(word[:(postion)]))
            else:
                if (word.find('年') == -1):
                    if (word.find('以下') != -1):
                        # XX万以下
                        postion = word.find('以下')
                        bottomSalary = str(float(word[:(postion - 5)]) * 10)
                    elif (word.find('以上') != -1):
                        # XX万以上
                        postion = word.find('以上')
                        bottomSalary = str(float(word[:postion - 5]) * 10)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        bottomSalary = str(float(word[:(postion)]) * 10)
                    else:
                        # XX万/月
                        postion = word.find('-')
                        bottomSalary = str(float(word[:(postion)]) * 10)

                else:
                    if (word.find('以下') != -1):
                        # XX万以下/年
                        postion = word.find('以下')
                        bottomSalary = str(float(word[:(postion - 5)]) / 1.2)
                    elif (word.find('以上') != -1):
                        postion = word.find('以上')
                        bottomSalary = str(float(word[:postion - 5]) / 1.2)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        bottomSalary = str(float(word[:(postion)]) / 1.2)
                    else:
                        # XX万/年
                        postion = word.find('-')
                        bottomSalary = word[:(postion)]
                        bottomSalary = str(float(bottomSalary) / 1.2)
            return bottomSalary

        if method == 'top':
            length = len(word)
            if (word.find('万') == -1):
                if (word.find('以下') != -1):
                    # XX千以下
                    postion = word.find('以下')
                    topSalary = str(float(word[:(postion - 5)]))
                elif (word.find('以上') != -1):
                    postion = word.find('以上')
                    topSalary = str(float(word[:postion - 5]))
                else:
                    # XX千/月
                    postion = word.find('-')
                    topSalary = str(float(word[(postion + 1):(length - 11)]))
            else:
                if (word.find('年') == -1):
                    if (word.find('以下') != -1):
                        # XX万以下
                        postion = word.find('以下')
                        topSalary = str(float(word[:(postion - 5)]) * 10)
                    elif (word.find('以上') != -1):
                        # XX万以上
                        postion = word.find('以上')
                        topSalary = str(float(word[:postion - 5]) * 10)
                    else:
                        # XX万/月
                        postion = word.find('-')
                        topSalary = str(float(word[(postion + 1):(length - 11)]) * 10)

                else:
                    if (word.find('以下') != -1):
                        # XX万以下/年
                        postion = word.find('以下')
                        topSalary = str(float(word[:(postion - 5)]) / 1.2)
                    elif (word.find('以上') != -1):
                        # XX万以上一年
                        postion = word.find('以上')
                        topSalary = str(float(word[:postion - 5]) / 1.2)
                    elif (word.find('+') != -1):
                        # XX万+
                        postion = word.find('+')
                        topSalary = str(float(word[:(postion)]) / 1.2)
                    else:
                        # XX万/年
                        postion = word.find('-')
                        topSalary = word[(postion + 1):(length - 11)]
                        topSalary = str(int(topSalary) / 1.2)
            return topSalary

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            passwd='mysql',
            db='scrapyDB',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)

    def close_spider(self, spider):
        try:
            # open the cursor
            self.cursor = self.conn.cursor()

            # get data from csv file
            # reload data
            f = open(r'job.csv', 'r')
            f.close()
            job_info = pandas.read_csv(r'job.csv', iterator=True,chunksize=1,
                                       header=None,names=
                                       ['job_name','company','address','bottom_salary','top_salary','salary','time'])

            # store data
            for i, job in enumerate (job_info):
                # use -1 or ' ' to fill NAN
                job = job.fillna({'job_name':'','company':'','address':'','time':''})
                job = job.fillna(-1)
                # transform series to list type
                job = job.values[0]

                sql = 'INSERT INTO tb_job(job_name,company,address,bottom_salary,top_salary,salary,time)' \
                      'VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                      job[6], job[2], job[3], job[1], job[5], job[0], job[6])
                self.cursor.execute(sql)
            self.conn.commit()

        finally:
            # close the connection
            self.conn.close()


    def process_item(self, item, spider):
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
        if(salary == None):
            raise DropItem("Dirty data %s" % item)

        # sort out data
        salary = ''.join(salary)
        item['bottomSalary'] = self.cut_word(salary, method='bottom')
        item['topSalary'] = self.cut_word(salary, method='top')

        # Connecting with local database


        # db = pymysql.connect(
        #     host='localhost',
        #     user='root',
        #     passwd='mysql',
        #     db='scrapyDB',
        #     charset='utf8',
        #     cursorclass=pymysql.cursors.DictCursor)
        # try:
        #     # open the cursor
        #     cursor = db.cursor()
        #     sql = 'INSERT INTO tb_job(job_name,company,address,bottom_salary,top_salary,salary,time)' \
        #           'VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (job_name,item['company'],item['address'],item['bottomSalary'],item['topSalary'],item['salary'],item['time'])
        #     # execute the sql
        #     cursor.execute(sql)
        #     db.commit()
        # finally:
        #     # close the connection
        #     db.close()

        return item


