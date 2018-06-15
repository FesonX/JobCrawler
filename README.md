# JobCrawler

_**To get English doc, please scroll down 
the page.**_


## 简介
-------------------------------
基于Python3的Scrapy爬虫项目, 主爬取网站为51Job, 次爬取网站为拉勾网

项目在Ubuntu17.10上开发, 在Mac OS上或其他Linux衍生系统上运行可能有少许命令上的不同.
不建议在Windows上运行本项目.

> 在项目最初的Commit中基于Python2, 但Python2对中文编码不友好,且未来将失去很多模块支持.

基于存储速度的考量,在最新的版本中, 项目使用MonogoDB存储,你仍然可以输出`*.csv`文件.

提供基于Django和HighCharts数据可视化项目, 详情请点击[JobDataViewer](https://github.com/FesonX/JobDataViewer)


**有问题欢迎邮箱(fesonx@foxmail.com)或issue,喜欢记得star**

## 关于Python3
-------------------------------
### 可以搜索廖雪峰, 参考学习Python3. 慕课网上亦有相关教程

## 关于Scrapy
-------------------------------

### 可以在官方网站获取Scrapy文档学习
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/overview.html
```

### 安装Scrapy
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/install.html#scrapy
```

## 运行
-------------------------------
### 安装相关依赖
#### 1. 安装Python3
项目使用Python3.6, 可以使用以下连接安装, 将文中的3.5改为3.6即可.
[ubuntu14.04安装python3.5并且将其设置为python3默认启动](https://blog.csdn.net/fireflychh/article/details/78195778)

#### 2. 使用virtualenv(也可以使用Anaconda或Pycharm管理)
Virtualenv允许多版本Python同时在电脑上共存, 安装完Python3及pip后
终端键入
```shell
# 安装
pip3 install virtualenv
# 创建虚拟环境
virtualenv spider-env
# 激活虚拟环境
source spider-env/bin/activate
# 退出
deactivate
```

#### 3. 安装库依赖
因为Scrapy依赖`Python.h`,在安装库依赖前在终端键入
```shell
 sudo apt-get install libpython3.6-dev
```
 然后安装依赖, 如果失败, 请逐条尝试
```shell
# 在JobCrawler/JobCrawler目录下
pip install -r requirements.txt
```

#### 4. 安装MongoDB
参照以下连接安装
[Install MongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/)

### 运行爬虫
终端`cd`到项目根目录, 键入
```shell
# -o job.csv为可选参数, 加入则输出到指定文件中
scrapy crawl jobCrawler -o job.csv
```


# JobCrawler

## Intro
---------------------------
Scrapy Project For Crawling Job Information on 51Job Based on Python3.

> (You can check out the commits before to get project based on Python2, 
but it's not recommended due to Python2 doesn't support Chinese very well
and many modules don't support Python2 any more.)

In the latest version, the project now use MongoDB to save data.


## About Scrapy
----------------------------

### Get docs from Scrapy(Chinese Ver. Avaiable)
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/overview.html
```
### Install Scrapy for your PC
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/install.html#scrapy
```


## Sample data
-----------------------------

>`job.csv` include job data about `python` from `51job`


## Run JobCrawler
------------------------------

### Install Python3

```
sudo add-apt-repository ppa:fkrull/deadsnakes

sudo apt-get update

sudo apt-get install python3.6
```
To make Python3.6 as default Python Version, read this [arcticle](https://blog.csdn.net/fireflychh/article/details/78195778)

### Install Virtualenv(Or Use Pycharm, Anaconda as lib manager)

```shell
# Install
pip3 install virtualenv
# Create
virtualenv spider-env
# Activate
source spider-env/bin/activate
# Quit
deactivate
```

### Install requirements
type this command first
```shell
 sudo apt-get install libpython3.6-dev
```
Because scrapy require `Python.h`

Than type`pip install -r requirements.txt`
If Failed, try open the `requirements.txt`, and  type `pip install` one by one.

### Install MongoDB
[Install MongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/)

### Run Spider
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