# JobCrawler

## Intro
Scrapy Project For Crawling Job Information on 51Job

## About Scrapy

### Get docs from Scrapy(Chinese Ver. Avaiable)
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/overview.html
```
### Install Scrapy for your PC
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/install.html#scrapy
```

## Simple data

>`job.csv` include job data about `python` from `51job`

## Version1.0

### Run JobCrawler
```python
scrapy crawl jobCrawler

# if u want to output the result to csv file, use this command instead:
scrapy crawl jobCrawler -o filename.csv

# u can change the spider name in /spider/spider.py
...
class JobSpider(Spider):
    # input spider name here
    name = 'jobCrawler'
    ...

```

## Version 1.1

### Now add primary key from website

```python
def parse(self, response):
        item = JobcrawlerItem()
        jobs = response.xpath('//*[@id="resultList"]/div[@class="el"]')
        for job in jobs:
            loader = JobItemLoader(item=JobcrawlerItem(), selector=job)
            # job_id field
            item['job_id'] = job.xpath('.//p/input/@value').extract()
            ...
```

### Now you can insert data into database via scrapy pipeline