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

## Version1.0

### Run JobCrawler
```
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


## Version2.0
#### Version Intro

1. Add new feature: data sort out and data store
   data store based on mysql
   features bulid on Scrapy's Pipeline module
2. New running program way: run `run.py`
3. Check out article `http://www.jianshu.com/p/17c9241acc71`

