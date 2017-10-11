# -*- coding: utf-8 -*-
from .defaults import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'USER': 'exingcai',
    'PORT': 20306,
    'HOST': '192.168.0.204',
    'NAME': 'alpha',
    'PASSWORD': 'uscj!@#',
}

MQ_HOST = '192.168.0.204'

HTTP_HOST = 'http://alert.a3.useonline.cn'


# 服务号 【点石成金】
WECHAT_APPID = 'wx3f67e479451b5eef'
WECHAT_APPSECRET = 'e3af32b6757b2326d62e03a7136db400'
# 获取 access_token 的 url
WECHAT_GET_ACCESS_TOKEN_URL = 'http://139.224.68.150:9020/api/wechat/accesstoken'
# 发送模板消息的url
WECHAT_SEND_TEMPLATE_MSG_URL = 'http://product.mp.useonline.cn/openapi/common/templatemessage'

# 微信授权的url
WECHAT_AUTH_URL = 'http://mp.useonline.cn/mp/redirect_alpha.html'

# 二维码有效时间
WECHAT_QR_EXPIRE_SECONDS = 1800
WECHAT_TEMPLATES = {
    'alert': {
        'id': 'MmRYvPPwvTSzZhl4QaPFZ--kDtdqNVYK-jMBezywn8Q',
        'args': ['first', 'keyword1', 'keyword2', 'keyword3', 'remark'],
        'desc': '报警信息',
    },
    'bind_mobile': {
        'id': 'U11OJhGASjJaHyUQmIsA906lmTzSNTA33ZKy07FPScg',
        'args': ['first', 'keyword1', 'keyword2', 'remark'],
        'desc': '账户绑定通知'
    }
}

# 手机认证前端[手机端]地址
QIAN_MOBILE_VALIDATION_URL = 'http://mp.useonline.cn/mp/pub/#/login?openId=%s&redirect=%s'
# 微信用户绑定信息接口
QIAN_GET_WECHAT_USER_INFO_URL = 'http://product.mp.useonline.cn/wechat/user/info'

# 主站前端入口
A3_FE_URL = 'http://alert.a3.useonline.cn/#/history'
A3_FE_REGISTER_URL = 'http://alert.a3.useonline.cn/#/register'
