# coding: utf-8
import os
import logging.config

from share.conf import config_module

jobs = ['jobs.alert.alert_history',
        'jobs.alert.alert_history_compensate']

alert_history_tpl = ''
alert_history_compensate_tpl = ''
WECHAT_APPID = config_module.WECHAT_APPID
WECHAT_SEND_TEMPLATE_MSG_URL = config_module.WECHAT_SEND_TEMPLATE_MSG_URL
template_id = config_module.WECHAT_TEMPLATES['alert']['id']
WECHAT_AUTH_URL = config_module.WECHAT_AUTH_URL
http = {'host': config_module.HTTP_HOST}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGER_DIR = os.path.normpath(os.path.join(BASE_DIR, "../../logs/schedule"))

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
            'filename': os.path.join(LOGGER_DIR, 'schedule_info.log'),
            'backupCount': 5,
            'maxBytes': 50 * 1024 * 1024,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGER_DIR, 'schedule_error.log'),
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
        'schedule': {
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
