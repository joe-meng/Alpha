# -*- coding: utf-8 -*-
from .defaults import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'USER': 'exingcai',
    'PORT': 20306,
    'HOST': '172.16.88.163',
    'NAME': 'alpha',
    'PASSWORD': 'uscj!@#',
}

MQ_HOST = '172.16.88.163'

HTTP_HOST = 'http://alert-test.a3.useonline.cn'


