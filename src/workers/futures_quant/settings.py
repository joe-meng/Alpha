#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-08-16

@author: zhoucuilian
"""
import logging.config
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGGER_DIR = os.path.normpath(
    os.path.join(BASE_DIR, "../../../logs/workers/futures_quant"))
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
            'filename': os.path.join(LOGGER_DIR, 'dojistar_info.log'),
            'backupCount': 5,
            'maxBytes': 50 * 1024 * 1024,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGER_DIR, 'dojistar_error.log'),
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
        'dojistarlog': {
            'handlers': ['file', 'error_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING_DICT)
logger = logging.getLogger("dojistarlog")
