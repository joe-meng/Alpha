# encoding: utf-8
from datetime import date, datetime
import logging
import requests

from s_common import Spider
from symbols.models import Symbol
from third_party_data.models import EnanchuData

logger = logging.getLogger(__name__)


class EnanchuSpider(Spider):
    code_list = ["837", "838", "836", "844", "846", "847", "848", "850", "851", "566", "527", "569", "810", "809",
                 "568", "812", "811", "522", "801", "800", "666", "665", "567", "814", "813", "853", "852", "842",
                 "841", "839", "834", "833", "832"]

    def _run(self):
        for code in self.code_list:
            url = 'http://www.enanchu.com/retrieveAjaxJsChartData.action?mainCategoryId=%s' % code
            logger.info('开始请求 %s' % url)
            resp = requests.get(url, timeout=5)

            if resp.status_code != 200:
                raise Exception('请求返回状态码非 200')

            resp = resp.json()
            symbol = 'ENANCHU_%s' % code

            # symbol 是否存在, 若不存在则新建
            symbol_obj = Symbol.objects.filter(symbol=symbol).first()
            if not symbol_obj:
                logger.info('symbol %s not exist, adding to symbol...' % symbol)
                symbol_obj = Symbol(
                    title=resp['mainLineName'],
                    symbol=symbol,
                    table_name='data_enanchu',
                    unit=resp['mainUnitText'],
                    source='南储商务网接口',
                    duration_unit='d'
                )
                symbol_obj.save()

            latest_record = EnanchuData.objects.filter(symbol=symbol).order_by('-date').first()
            if latest_record:
                logger.info('%s 数据库最新数据日期为 %s, 请求返回最新数据日期为 %s' % (
                    symbol,
                    latest_record.date,
                    date.strftime(
                        datetime.fromtimestamp(resp['mainAxis'][-1][0] / 1000).date(),
                        '%Y-%m-%d'
                    )
                ))
                rows_to_insert = list(filter(
                    lambda i: datetime.fromordinal(latest_record.date.toordinal()).timestamp() < i[0] / 1000,
                    resp['mainAxis'])
                )
            else:
                logger.info('%s 数据库无数据, 全部保存到数据库' % symbol)
                rows_to_insert = resp['mainAxis']

            if len(rows_to_insert):
                logger.info('开始写入新数据 %s 条' % len(rows_to_insert))
                enanchu_record_list = []
                for row in rows_to_insert:
                    day = datetime.fromtimestamp(row[0] / 1000).date()
                    enanchu_record_list.append(EnanchuData(
                        amount=row[1],
                        symbol=symbol,
                        date=day
                    ))
                EnanchuData.objects.bulk_create_all_envs(enanchu_record_list, logger=logger)
