# -*- coding: utf-8 -*-
import os
"""
HOST = "211.152.46.43"

mysql_conf['host'] = HOST
mysql_conf['port'] = 3306
mysql_conf['db_name'] = 'ie'
mysql_conf['user'] = 'deploy'
mysql_conf['pwd'] = '9i[1sF&#2>nBo!*z'
"""
# 默认的配置为开发环境
# DATABASES = {}
DATABASES = {
    'miaoyichao': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'exingcai',
        'PORT': 20306,
        'HOST': '172.16.88.140',
        'REDIS_HOST': '172.16.88.140',
        'REDIS_PORT': 6379,
        "REDIS_PWD": 'test123',
        "REDIS_DB": 0,
        'NAME': 'alpha',
        'PASSWORD': 'uscj!@#',
        'MQ_HOST': '172.16.88.140',
    },
    "default":{
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'exingcai',
        'PORT': 20306,
        'HOST': '172.16.88.140',
        'NAME': 'alpha',
        'PASSWORD': 'uscj!@#',
        'MQ_HOST': '172.16.88.140',
        'REDIS_HOST': '172.16.88.140',
        'REDIS_PORT': 6379,
        "REDIS_PWD": 'test123',
        "REDIS_DB": 0,
    },
    'develop':{
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'exingcai',
        'PORT': 20306,
        'HOST': '172.16.88.140',
        'NAME': 'alpha',
        'PASSWORD': 'uscj!@#',
        'MQ_HOST': '172.16.88.140',
        'REDIS_HOST': '172.16.88.140',
        'REDIS_PORT': 6379,
        "REDIS_PWD": 'test123',
        "REDIS_DB": 0,
    },
    'test':{
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'exingcai',
        'PORT': 20306,
        'HOST': '172.16.88.163',
        'NAME': 'alpha',
        'PASSWORD': 'uscj!@#',
        'MQ_HOST': '172.16.88.163',
        'REDIS_HOST': '172.16.88.163',
        'REDIS_PORT': 6379,
        "REDIS_PWD": 'test123',
        "REDIS_DB": 0,
    },
    'online':{
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'exingcai',
        'PORT': 20306,
        'HOST': '192.168.0.204',
        'NAME': 'alpha',
        'PASSWORD': 'uscj!@#',
        'MQ_HOST': '192.168.0.204',
        'REDIS_HOST': '192.168.0.204',
        'REDIS_PORT': 6379,
        "REDIS_PWD": 'test123',
        "REDIS_DB": 0,
    }
}

SPIDER_WRITING_DB_NAMES = ['develop', 'test', 'online']

def get_env():
    env = os.environ["ALPHA_ENV"]
    return DATABASES.get(env, DATABASES["default"])
    # return DATABASES["online"]
MQ_HOST = '172.16.88.140'

HTTP_HOST = 'http://172.16.88.140:9100'



# 测试服务号 [优运]
WECHAT_APPID = 'wxe8cae73034a7fc5e'
WECHAT_APPSECRET = 'b2ed940c60daa57c25b7a04606e03195'
# 获取 access_token 的 url
WECHAT_GET_ACCESS_TOKEN_URL = 'http://172.16.88.162:9020/api/wechat/accesstoken'
# 发送模板消息的url
WECHAT_SEND_TEMPLATE_MSG_URL = 'http://pub.weixin.useonline.cn/openapi/common/templatemessage'
# 微信授权的url
WECHAT_AUTH_URL = 'http://qian.useonline.cn/mp/redirect_alpha.html'
# 二维码有效时间
WECHAT_QR_EXPIRE_SECONDS = 1800
WECHAT_TEMPLATES = {
    'alert': {
        'id': 'jGbwWa7_hbB5uP4Ae1OzOZzHCmnOa74b45h837MsfQ0',
        'args': ['first', 'keyword1', 'keyword2', 'keyword3', 'remark'],
        'desc': '报警信息',
    },
    'bind_mobile': {
        'id': 'WLjqMTltW5fRoMTSa-qFKEcEyIc6lWLQAN-_tF8thv0',
        'args': ['first', 'keyword1', 'keyword2', 'remark'],
        'desc': '账户绑定通知'
    }
}

# 手机认证前端[手机端]地址
QIAN_MOBILE_VALIDATION_URL = 'http://qian.useonline.cn:9060/mp/pub/#/login?openId=%s&redirect=%s'
# 微信用户绑定信息接口
QIAN_GET_WECHAT_USER_INFO_URL = 'http://172.16.88.144:8012/wechat/user/info'

# 主站前端入口
A3_FE_URL = 'http://alert-test.a3.useonline.cn/#/history'
A3_FE_REGISTER_URL = 'http://alert-test.a3.useonline.cn/#/register'
