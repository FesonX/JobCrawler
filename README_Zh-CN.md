# JobCrawler

## 简介
-------------------------------
基于Python3的Scrapy爬虫项目, 主爬取网站为51Job, 次爬取网站为拉勾网
> 在项目最初的Commit中基于Python2, 但Python2对中文编码不友好,且未来将失去很多模块支持.

在最新的版本中, 项目使用MonogoDB存储

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
