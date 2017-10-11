# Alpha 项目说明
有色行业数据、资讯整合



## 数据项目
数据整理、分析、提供预警

1. 各个交易所的交易数据（k线、持仓、交易量）
2. 各地库存
3. 升贴水
4. 外汇汇率
5. 仓单
6. 产量

### 数据流
- 通过 CTP 数据每分钟驱动注册的所有计算，推送预警信息
- 全过程通过 MQ 连接

### 数据源
- CTP
- 爬虫
- 万德资讯



## 资讯项目
资讯整合，提供搜索、热点推荐功能


### 数据源
- 爬虫




# Alpha 架构说明
包括几个顶级模块
- api
    - Django 项目
    - 负责 MySQL 建模，支持其他模块调用其模型
    - 对外提供 web 服务
- data_spider
    - 数据爬虫
- info_spider
    - 资讯爬虫
- workers
    - MQ 队列的消费者
- share
    - 全局共享的配置，包括数据库、MQ 等
- logs
    - 日志存储


# symbol 命名
根据不同的数据来源进行命名
- wind
    - S开头
    - M开头
- 爬虫
    - USE开头
    - 南储数据 ENANHCU开头
- 预计算
    - PE开头
        - 分钟数据 PE0开头
        - 日数据  PE1开头
        - 从CTP直接过来的价格数据 PE2开头
- 人工录入数据
    - MA开头


# Usage
使用时需要指定环境变量 DJANGO_SETTINGS_MODULE 为 `alpha.settings.env`, 其中 env 为 defaults / develop / test / prod

资讯模块增加mongo的索引:
    直播:
        db.live.createIndex({"top_tag" : -1, "craw_time" : -1}, {'name': 'live_top_time_desc'})

        db.live.createIndex({"top_tag" : -1,"pub_time" : -1}, {'name': 'live_top_pub_desc'})

        db.live.createIndex({"top_tag" : -1,"click_count" : -1, "pub_time" : -1}, {'name': 'live_top_click_desc'})
    资讯:
        db.news.createIndex({"top_tag" : -1, "craw_time" : -1}, {'name': 'news_top_time_desc'})

        db.news.createIndex({"top_tag" : -1,"pub_time" : -1}, {'name': 'news_top_pub_desc'})

        db.news.createIndex({"top_tag" : -1,"click_count" : -1, "pub_time" : -1}, {'name': 'news_top_click_desc'})


# 部署

    fab -R develop deploy

- -R 指定需要部署的服务器
- deploy后面可以跟二个参数:
    - branch 分支名(default:develop)
    - is_sudo 是否sudo操作(default:True)