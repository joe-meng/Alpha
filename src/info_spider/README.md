# Usage  环境都是python3

# 部署的时候需要创建文件日志目录
## 日志目录在项目目录同级logs/*.log

爬虫获取中国有色网的文章
使用方法
```
cd websitespider && scrapy crawl cnmn
```
获取上海有色网的直播和要闻
使用方法

```
cd websitespider/interface && python smm.py
```

获取华尔街见闻的直播
使用方法

```
cd websitespider/interface && python wallstreet.py
```

# 比如要爬公众号*今日有色*
在命令行输入，可以爬取最近一批文章
```
scrapy crawl wechat -a username=今日有色
```

## 有色相关公众号
今日有色
海通有色
南储商务网
文韬武略话有色
