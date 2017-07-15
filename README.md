# JobCrawler
Scrapy Project For Crawling Job Information on 51Job

## Version1.0

### Instal Scrapy for your PC
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/install.html#scrapy
```

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
