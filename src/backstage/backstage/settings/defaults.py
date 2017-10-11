# -*- coding: utf-8 -*-
import os
import sys

from share.settings.defaults import *

# BASE_DIR 为 src/backstage
root_path = os.path.abspath(__file__)
while os.path.basename(root_path) != 'src':
    root_path = os.path.dirname(root_path)
root_path = os.path.join(root_path, 'backstage')
BASE_DIR = root_path

SECRET_KEY = '&__&-09ga15=(8s)dc^65^f(e4r^_$wbyo8jze8uwb&s^c&$ud'

DEBUG = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'sidebar',
    'common',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backstage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backstage.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'zh-HANS'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = False
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

EMAIL_HOST = 'smtp.ym.163.com'
EMAIL_HOST_USER = 'noreply@1b2b.cn'
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD', '111111')
SERVER_EMAIL = 'Alpha程序报错 <yinzheduan@1b2b.cn>'

ADMINS = [
    ('Yin', 'yinzheduan@1b2b.cn'),
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'Security-Token',
    # 'use_info_ms-token',
    # 'HTTP_USECLOUD_TOKEN'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'),
    'PAGE_SIZE': 100,
    'UNICODE_JSON': True,
    'DATETIME_FORMAT' : '%Y-%m-%d %H:%M:%S',
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },

}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(name)s '
                      '[%(lineno)d]: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../../logs/backstage/info.log'),
            'backupCount': 5,
            'maxBytes': 50 * 1024 * 1024,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'wechat': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'use_info_ms': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'formula': {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

MONGO_DB_SETTINGS = {'host': '127.0.0.1', 'port': 27017, }
MONGO_DB_NAME = 'data'

ALI_OSS_ACCESS_KEY_ID = 'ioXmmkNaeY1QQ3Qx'
ALI_OSS_ENDPOINT = 'oss-cn-shanghai.aliyuncs.com'
ALI_OSS_ACCESS_KEY_SECRET = 'mmO8fsgpSS2vfmADX3VtKCLRkhWZoi'
ALI_OSS_BUCKET_NAME = 'chengjin-spider'
FATHER_URL = 'http://chengjin-spider.oss-cn-shanghai.aliyuncs.com/'

LOCAL_URL = 'http://127.0.0.1:9500/'


KV_OBJECT_DEFAULT_VARIETIES_SUBSCRIPTION_KEY = 'default_varieties_subscription'
