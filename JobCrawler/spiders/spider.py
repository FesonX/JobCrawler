# coding=utf-8
from scrapy import Request
from scrapy.spiders import Spider
# 下面的import是正确的，但在pycharm中会有红色警告横线，改用..items
# from douban.items import DoubanMovieItem, JobItem
from ..items import JobcrawlerItem, JobItemLoader


class JobSpider(Spider):
    name = 'JobCrawler'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        keyword = raw_input('请输入职位关键词：')
        url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=&keyword=%s' \
              '&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9' % (keyword)
        yield Request(url, headers=self.headers)

    def parse(self, response):

        item = JobcrawlerItem()
        jobs = response.xpath('//*[@id="resultList"]/div[@class="el"]')
        for job in jobs:
            loader = JobItemLoader(item=JobcrawlerItem(), selector=job)
            # strip去除前后空格,extract的结果是list，用join结合为字符串再进行strip，避免中文乱码
            job_name = job.xpath('.//p/span/a/text()').extract()
            item['job_name'] = ''.join(job_name).strip()
            item['company'] = job.xpath('.//span[@class="t2"]/a/text()').extract()
            item['address'] = job.xpath('.//span[@class="t3"]/text()').extract()
            item['salary'] = job.xpath('.//span[@class="t4"]/text()').extract()
            item['time'] = job.xpath('.//span[@class="t5"]/text()').extract()
            yield item
            # job_name = job.xpath('.//p/span/a/text()').extract()
            # loader.add_xpath('job_name', './/p/span/a/text()')
            # loader.add_xpath('company', './/span[@class="t2"]/a/text()')
            # loader.add_xpath('address', './/span[@class="t3"]/text()')
            # loader.add_xpath('salary', './/span[@class="t4"]/text()')
            # loader.add_xpath('time', './/span[@class="t5"]/text()')

            # yield loader.load_item()
        # next_url = response.xpath('/html/body/div[2]/div[6]/div/div/div/ul/li[8]/a/@href').extract()
        next_url = response.xpath('//div[@class="p_in"]/ul/li[8]/a/@href').extract()
        if next_url:
            # 注意extract是list，所以要转化为str
            next_url = ''.join(next_url)
            yield Request(next_url, headers=self.headers)

