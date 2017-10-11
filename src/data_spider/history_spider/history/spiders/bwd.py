# -- coding: utf-8 --
from datetime import datetime
import json

import logging
from scrapy import Spider, Request
from future.models import FutureBWDSummary


logger = logging.getLogger(__name__)


class SmmBwdSpider(Spider):
    name = 'bwd'
    handle_httpstatus_list = [404]

    def start_requests(self):
        # 铜
        # url = 'https://hq.smm.cn/getdata/premium/history/201102250185/2014-08-21/2017-08-21'
        # 铝
        url = 'https://hq.smm.cn/getdata/premium/history/201102250563/2014-08-21/2017-08-21'
        yield Request(url, callback=self.parse_json)

    def parse_json(self, response):
        source = 'smm'
        symbol = 'USE00146'
        varieties = 'Al'

        if response.status == 200:
            json_response = json.loads(response.text)['premium_history']

            for row in json_response:
                d = datetime.strptime(row['RenewDate'], '%Y-%m-%d').date()
                try:
                    bwd, created = FutureBWDSummary.objects.update_or_create_all_envs(
                        varieties=varieties,
                        future='1m',
                        source=source,
                        date=d,
                        duration_unit='d',
                        symbol=symbol,
                        defaults={
                            'price_high': row['Highs'],
                            'price_low': row['Low'],
                            'price': row['Average'],
                        }
                    )
                    self.logger.info(('%s %s %s %s 成功' % (varieties, source, d, '插入' if created else '更新')).center(80, '*'))
                except Exception as e:
                    self.logger.error(('%s %s %s 写入/更新失败 %s' % (varieties, source, d, e)).center(80, '*'))
