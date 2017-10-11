# -- coding: utf-8 --
import json
from collections import OrderedDict
from datetime import datetime

import re

import logging
import requests

from future.models import FutureHolding

logger = logging.getLogger(__name__)


def crawl_easymoney_lme():
    """
    eastmoney lme 持仓 | 铜、铝、镍、锌
    """

    source = 'easymoney_lme'
    metal_lme_mapping = OrderedDict((
        ('Cu', {
            'match': 'LCPS0',
            'symbol': 'USE00034',
        }),
        ('Al', {
            'match': 'LALS0',
            'symbol': 'USE00035',
        }),
        ('Ni', {
            'match': 'LNKS0',
            'symbol': 'USE00036',
        }),
        ('Zn', {
            'match': 'LZNS0',
            'symbol': 'USE00037',
        }),
    ))
    ids = [i['match'] for i in metal_lme_mapping.values()]
    url = 'http://hq2gjqh.eastmoney.com/EM_Futures2010NumericApplication/index.aspx?type=z&jsname=spqhdata&ids=%s' % ','.join(ids)

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    response = json.loads(re.findall(r'\[.*\]', response.text)[0])

    for i, metal in enumerate(metal_lme_mapping):
        line = response[i].split(',')
        FutureHolding.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            future='3m',
            date=datetime.strptime(line[-2], '%Y-%m-%d %H:%M:%S'),
            symbol=metal_lme_mapping[metal]['symbol'],
            defaults={
                'amount': line[16],
            }
        )

