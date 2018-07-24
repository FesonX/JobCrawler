# coding=utf-8
import re
import json
from scrapy import Request
from scrapy.spiders import Spider
# 下面的import是正确的，但在pycharm中会有红色警告横线，改用..items
from ..items import JobcrawlerItem, JobItemLoader
import pandas as pd 
from pymongo import MongoClient


class JobSpider(Spider):
    name = 'jobCrawler'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):

        file_csv = pd.read_csv('field.csv')
        data = []
        for i in file_csv.values:
            # 把DataFrame格式转为list
            data.append(i[1])

        area_top = {'010000': '北京', '020000': '上海', '030200': '广州', '040000': '深圳', \
        '200200': '西安', '180200': '武汉', '080200': '杭州', '070200': '南京', '090200': '成都',\
        '060000': '重庆', '230200': '沈阳', '120300': '青岛', '080300': '宁波', '170200': '郑州', \
        '050000': '天津', '070300': '苏州', '190200': '长沙', '070400': '无锡', '030800': '东莞', '01': '珠三角'}

        area_top.keys()

        # 珠三角地区 惠州、汕头、珠海、佛山、中山、江门、湛江、肇庆、清远
        #area_zhusanjiao = 01

        # while(1):
        #     area = input('请选择职位地区数字：1.全国， 2.东莞')

        #     if(str(area) != '1' and area != '2'):
        #         print("输入有误，请重新输入")
        #     else:
        #         break
        allowed_domain = ['http://search.51job.com']
        for keyword in data:
            # if area == '1':
            #     url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&keyword=%s' \
            #    '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9' % (keyword)
            # if(area == '2'):
            #     url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=030800&keyword=%s' \
            #    '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9' % (keyword)
            for area in area_top.keys():
                url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=%s&keyword=%s' \
                '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9' % (area, keyword)
                # 使用meta传递key_word搜索关键词
                yield Request(url, headers=self.headers, meta={'key_word': keyword, 'area': area_top[area]})   


    def parse(self, response):
        item = JobcrawlerItem()
        jobs = response.xpath('//*[@id="resultList"]/div[@class="el"]')

        for job in jobs:
            client = MongoClient()
            db = client['Spider']
            coll = db.job
            from scrapy.exceptions import CloseSpider
            import datetime

            item['job_id'] = job.xpath('.//p/input/@value').extract()
            
            if(coll.find_one() is not None):
                if (coll.find_one()['job_id'] == item['job_id']):
                    raise CloseSpider("Duplicate Data")

            item['create_time'] = job.xpath('.//span[@class="t5"]/text()').extract()
            item['company'] = job.xpath('.//span[@class="t2"]/a/text()').extract()
            # strip去除前后空格,extract的结果是list，用join结合为字符串再进行strip，避免中文乱码
            job_name = job.xpath('.//p/span/a/text()').extract()
            item['job_name'] = ''.join(job_name).strip()
            # 添加51Job缺失的年份,在跨年份的爬取可能会出错
            day = ''.join(item['create_time'])
            day = datetime.datetime.strptime(day, '%m-%d')
            day = day.replace(datetime.date.today().year)
            item['create_time'] = day
            item['key_word'] = response.meta['key_word']
            item['job_city'] = job.xpath('.//span[@class="t3"]/text()').extract()
            item['area'] = response.meta['area']
            item['salary'] = job.xpath('.//span[@class="t4"]/text()').extract()
            yield item
        
        next_url = response.xpath('//div[@class="p_in"]/ul/li[8]/a/@href').extract()
        if next_url:
            # 注意extract是list，所以要转化为str
            next_url = ''.join(next_url)
            yield Request(next_url, headers=self.headers, meta={'key_word': response.meta['key_word']})
