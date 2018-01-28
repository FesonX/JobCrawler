# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spider import Spider

from ..items import EntranceItem


class EntranceSpider(Spider):
    name = 'entrance'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    start_urls = ['https://www.lagou.com/']

    def start_request(self):
        yield Request(self.start_urls, headers=self.headers)

    def parse(self, response):
        item = EntranceItem()
        
        keys = response.xpath('//*[@id="sidebar"]/div/div[1]/div[2]/dl')
        for key in keys:
            # 获取当前领域的关键词
            key_list = key.xpath('.//dd/a/text()').extract()
            for l in key_list:
                item['key_word'] = l
                # 同一个领域
                item['key_field'] = key.xpath('.//dt/span/text()').extract()
                yield item