# -- coding: utf-8 --
from datetime import datetime, timedelta

import MySQLdb
from django.conf import settings
from django_extensions.management.jobs import BaseJob

import logging

from future.jobs.future import exchange_rate_mapping
from future.models import FuturePrice, FutureBWD, FutureExchangeRate
from spot.models import SpotExchangeRate

logging.basicConfig(
    format='%(asctime)s %(name)s[%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

old_db_settings = settings.DATABASES['local_daily_data']

conn = MySQLdb.connect(
    host=old_db_settings['HOST'],
    user=old_db_settings['USER'],
    db=old_db_settings['NAME'],
    passwd=old_db_settings['PASSWORD'],
    cursorclass=MySQLdb.cursors.DictCursor
)
cursor = conn.cursor()


class Job(BaseJob):
    help = "import future data from ie history mysql table [spot_info]"

    def execute(self):
        start = datetime.now()

        # 遍历 daily_data
        logging.info('开始获取 spot_info 数据')
        cursor.execute('select * from spot_info')
        data = cursor.fetchall()
        logging.info('数据获取完毕, 得到%s条数据' % len(data))

        price_list = []
        holding_list = []
        warehouse_receipt = []
        inventory = []
        exchange_rate_list = []

        logging.info('开始对应到 django model')

        for row in data:
            if datetime.now() - start > timedelta(seconds=10):
                logging.info('已对应 %s 条数据' % len(price_list))
                start = datetime.now()

            metal = metal_mapping[row['type']]
            date = row['date_of_record'] or row['crawl_time'].date()
            time = row['crawl_time'].time() if row['crawl_time'] else None
            created_at = row['crawl_time']

            for future, column in exchange_rate_mapping.items():
                rate = SpotExchangeRate(
                    currency='USD',
                    price=row[column],
                    created_at=created_at,
                    source='boc',
                    date=date,
                    time=time,
                )
                if future == '1w':
                    rate.price_buy = row['week_exchange_buy']
                if future == '3m':
                    rate.price_buy = row['three_mon_exchange_buy']
                if rate.price_buy or rate.price or rate.price_sell:
                    exchange_rate_list.append(rate)

            if row['huabei_avg_bwd']:
                price_list.append(FutureBWD(
                    varieties=metal,
                    future='1m',
                    date=date,
                    time=time,
                    source='huabei',
                    price=row['huabei_avg_bwd'],
                    created_at=created_at,
                    change=row['change'],
                ))

            if row['lme_3']:
                price_list.append(FuturePrice(
                    id=row['id'],
                    source='lme',
                    future='3m',
                    price=row['lme_3'],
                    date=date,
                    time=time,
                    created_at=created_at,
                    contract=row['agreement_3'],
                    varieties=row['type'],
                ))

            if row['bwd']:
                bwd_list.append(FutureBWD(
                    varieties=row['type'],
                    contract=row['agreement_1'],
                    future='1m',
                    date=date,
                    time=time,
                    source='shmet',
                    price=row['bwd'],
                    created_at=created_at,
                    change=row['change'],
                ))


        logging.info('已对应完毕')
        logging.info('开始写入数据库')

        batch = 5000
        count = 0
        while count * batch <= len(data):

            if datetime.now() - start > timedelta(seconds=30):
                logging.info('已写入 %s 条数据' % (count * batch))
                start = datetime.now()

            i, j = count * batch, (count + 1) * batch
            FuturePrice.objects.bulk_create(price_list[i:j])
            FutureExchangeRate.objects.bulk_create(exchange_rate_list[i:j])
            FutureBWD.objects.bulk_create(bwd_list[i:j])
            count += 1

        logging.info('所有数据写入完毕')
        # FutureHolding.objects.create(
        #     code = models.CharField('Cu1706', max_length=16)
        #     amount = models.DecimalField('持仓量', decimal_places=2, max_digits=10)
        #     change = models.DecimalField('持仓量变化', decimal_places=2, max_digits=10)
        #     future=future,
        #     created_at=row['created_at'],
        #     source='boc',
        #     date=date,
        #     amount=,
        # )


metal_mapping = {
    1: 'Cu',
    2: 'Al',
    3: 'Zn',
    4: 'Ni'
}
