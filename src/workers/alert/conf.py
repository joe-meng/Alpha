# coding: utf-8
import os
import logging.config

from share.conf import config_module
from workers.share.consumer import ConsumerConf


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
users_yaml = os.path.join(BASE_DIR, 'etc/users.yaml')
mysql = {'host': config_module.DATABASES['default']['HOST'],
         'port': config_module.DATABASES['default']['PORT'],
         'user': config_module.DATABASES['default']['USER'],
         'password': config_module.DATABASES['default']['PASSWORD'],
         'db': config_module.DATABASES['default']['NAME'],
         'charset': 'utf8',
         'timeout': 7200}
consumer_conf = ConsumerConf(host=config_module.MQ_HOST,
                             exchange='useonline.alpha.analysis',
                             exchange_type='topic',
                             routing_key='calculation',
                             queue='queue.calculation')
wechat = {'corpId': 'wx2a0ab93f2f8a53b1',
          'corpSecret': 'GK8nlpTicB0-gKiRledQe46OfUDjiPMVjdtgd_LeJAzLC3KkdrbxyvXmbPw0RX89',
          'agentId': 12}
http = {'host': config_module.HTTP_HOST}
template_id = config_module.WECHAT_TEMPLATES['alert']['id']
WECHAT_SEND_TEMPLATE_MSG_URL = config_module.WECHAT_SEND_TEMPLATE_MSG_URL
WECHAT_APPID = config_module.WECHAT_APPID
WECHAT_AUTH_URL = config_module.WECHAT_AUTH_URL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

LOGGER_DIR = os.path.normpath(
    os.path.join(BASE_DIR, "../../../logs/workers/alert"))
if not os.path.exists(LOGGER_DIR):
    os.makedirs(LOGGER_DIR)

LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
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
            'filename': os.path.join(LOGGER_DIR, 'alert_info.log'),
            'backupCount': 5,
            'maxBytes': 50 * 1024 * 1024,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGER_DIR, 'alert_error.log'),
            'backupCount': 5,
            'maxBytes': 50 * 1024 * 1024,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'alert': {
            'handlers': ['file', 'error_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
            },
    'root': {'handlers': ['file', 'error_file', 'console'],
             'level': 'INFO',
             'propagate': True}
}

logging.config.dictConfig(LOGGING_DICT)


ALERT_FILTERS = ['filter.AlertFilter']
ALERT_VIEWERS = ['viewer.SubscriberViewer']
