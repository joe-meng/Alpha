# encoding: utf-8
import os
from datetime import date, timedelta
import logging
import pandas as pd

from WindPy import w
from s_common import Spider
from symbols.models import Symbol
from third_party_data.models import WindData

logger = logging.getLogger(__name__)


def start_wind():
    os.system('python start_wind.py')


class WindSpider(Spider):
    def __init__(self, wind_account):
        self.wind_account = wind_account
        super(WindSpider, self).__init__()

    def _run(self):
        start_wind()

        # 获取需要抓取的 symbol 列表
        symbols = Symbol.objects.filter(
            table_name='data_wind',
            is_disabled=False,
            wind_account=self.wind_account
        ).order_by('symbol').values('symbol').distinct()
        logger.info('found %s symbols for wind_account: %s' % (symbols.count(), self.wind_account))

        for symbol in symbols:
            date_start = date(2008, 1, 1)

            # 计算该 symbol 抓取的时间区间
            latest_record = WindData.objects.filter(symbol=symbol['symbol']).order_by('-date').first()
            if latest_record:
                logger.info('%s up to %s' % (symbol['symbol'], latest_record.date))
                if latest_record.date >= date.today():
                    continue
                date_start = latest_record.date

            date_end = self.date_end

            # 抓取数据
            try:
                df = self.fetch_wind_data(symbol['symbol'], date_start, date_end)
            except Exception as e:
                logger.error(e.args[0])
                continue
            self.store_wind_data(symbol['symbol'], df)

    def fetch_wind_data(self, symbol, date_start, date_end):
        w.start()
        resp = w.edb([symbol], date_start, date_end)
        if resp.ErrorCode != 0:
            raise Exception('fetching %s [%s ~ %s] failed, status code: %s' % (
            symbol, self.date_start, self.date_end, resp.ErrorCode))
        logger.info('fetching %s [%s ~ %s] success' % (symbol, self.date_start, self.date_end))
        df = pd.DataFrame(resp.Data, columns=resp.Times, index=resp.Codes)
        return df

    def store_wind_data(self, symbol, df):
        for d, item in df.to_dict().items():
            for s, amount in item.items():
                if not pd.isnull(amount):
                    WindData.objects.update_or_create_all_envs(
                        logger,
                        symbol=symbol,
                        date=d,
                        defaults={
                            'amount': amount
                        }
                    )
