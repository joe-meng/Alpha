# -*- coding: utf-8 -*-
from .defaults import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'USER': 'deploy',
    'PORT': 3306,
    'HOST': '211.152.46.43',
    'NAME': 'test_alpha',
    'PASSWORD': '9i[1sF&#2>nBo!*z',
}

MQ_HOST = '172.16.88.140'
