# JobCrawler

## 简介
基于Python3的Scrapy爬虫项目, 主爬取网站为51Job, 次爬取网站为拉勾网
> 在项目最初的Commit中基于Python2, 但Python2对中文编码不友好,且未来将失去很多模块支持.

在最新的版本中, 项目使用MonogoDB存储

## 关于Python3
### 可以搜索廖雪峰, 参考学习Python3. 慕课网上亦有相关教程

## 关于Scrapy

### 可以在官方网站获取Scrapy文档学习
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/overview.html
```

### 安装Scrapy
```
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/install.html#scrapy
```

## 运行
```python
scrapy crawl jobCrawler

# 如果你想要输出csv文件, 使用以下命令:
scrapy crawl jobCrawler -o filename.csv

# 你可以在 /spider/spider.py 中修改爬取命令的名字
...
class JobSpider(Spider):
    # input spider name here
    name = 'jobCrawler'
    ...

```

本项目使用csv文件作为整个爬取的入口, 你需要在命令行中切换至
`/spspider`文件夹, 再运行爬取命令.
