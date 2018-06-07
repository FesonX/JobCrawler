# JobCrawler

## Intro
Scrapy Project For Crawling Job Information on 51Job Based on Python3.

> (You can check out the commits before to get project based on Python2, 
but it's not recommended due to Python2 doesn't support Chinese very well
and many modules don't support Python2 any more.)

In the latest version, the project now use MongoDB to save data.

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


## Run JobCrawler
Before running the Spider, type`pip install -r requirements.txt` in terminal to install requirements.
**type `cd` to the root directory of the project because of the file `field.csv`**

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


## Version Update Information

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

## Version 1.2

### Now Coding with Python3

### Now Develop with Scrapy 1.5
But I haven't found it any incompatible with old ver.

### Add new Spider to the Project
Source Code in `JobCrawler/spiders/entrance.py`
Also add new Scrapy field for the new spider, source code in `JobCrawler/items.py`

### Fix some bugs in Pipeline
**Here is what bugs fixed**
1. str to float error(*because of the string Segmentation ERROR*)
2. all spiders share the same pipeline method


## Version 1.3

### Now use Mongodb for saving data
MongoDB is a NoSQL Database

If U want to see the difference between MongoDb and MySQL, check out the past Ver.

When use Mysql for saving data, the time for closing spider will be much longer than mongodb.

### Fix DateTime Field Error
**Here is the detail**
In the past ver., scrapy Field `create_time` is save like `03-09`
without year because the website doesn't provide.

This bug cause other problems in my project I built recently.

Now I fixed it with the following code in `pipeline.py`:

```python
def process_item(self, item, spider):
    import datetime
    ...
    # sort out data
    ...
    day = ''.join(item['create_time'])
            day = datetime.datetime.strptime(day, '%m-%d')
            day = day.replace(datetime.date.today().year) 
            item['create_time'] = day
    ...

```

And config in `settings.py`

```python
...

MONGO_HOST = "127.0.0.1" #主机IP
MONGO_PORT = 27017       #端口号 
MONGO_DB = "Spider"      #库名
MONGO_COLL = "jobinfo"   #collection名
# MONGO_USER = ""
# MONGO_PSW = ""

...

```

### Add salary_avg Field

The project I built recently is a Django project for data visualization.

I need to reduce the compute time in that project as much as posssible to get faster
when user visit the page.