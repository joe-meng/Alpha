# encoding: utf-8
from datetime import date, timedelta
import logging
import json

import pandas as pd
import requests

from s_common import Spider
from symbols.models import Symbol
from third_party_data.models import DataShfeDayKLine

logger = logging.getLogger(__name__)

varieties_mapping = { '强麦': '强麦', '强筋小麦': '强麦', '普麦': '普麦', '硬麦': '普麦', '白小麦': '普麦', '棉花': '棉花', '棉':'棉花', '白糖': '白糖', '白砂糖': '白糖', '甲醇': '甲醇', '玻璃': '玻璃', '油菜籽': '油菜籽', '菜籽粕': '菜粕', '菜粕': '菜粕', '菜籽油': '菜籽油', '粳稻': '粳稻', '早籼稻': '早籼稻', '晚籼稻': '晚籼稻', '动力煤': '动力煤', '铁合金': '铁合金', '锰硅': '锰硅', '硅铁': '硅铁', 'PTA': 'PTA', '玉米': '玉米', '豆油': '豆油', '大豆': '豆油', '豆一': '豆一', '大豆1号': '豆一', '大豆2号': '豆二', '豆二': '豆二', '豆粕': '豆粕', 'PVC': 'PVC', '聚氯乙烯': 'PVC', '焦煤': '焦煤', '聚丙烯': '聚丙烯', '纤维板': '纤维板', '胶合板': '胶合板', '铁矿石': '铁矿石', '鸡蛋': '鸡蛋', '焦炭': '焦炭', '棕榈油': '棕榈油', 'LLDPE': 'LLDPE', '聚乙烯': 'LLDPE', '玉米淀粉': '玉米淀粉', '铜': 'Cu', '铝': 'Al', '铅': 'Pb', '锌': 'Zn', '镍': 'Ni', '锡': 'Sn', '天然橡胶': 'Ru', '燃料油': 'Fu', '黄金': 'Au', '螺纹钢': 'Rb', '线材': 'Wr', '白银':'Ag', '沥青': 'Bu', '热轧卷板': 'Hc', }

class ShfeSpider(Spider):

    def _run(self):
        latest_record = DataShfeDayKLine.objects.order_by('-date').first()
        current_date = date(2008, 1, 1) if not latest_record else latest_record.date + timedelta(days=1)
        logger.info('从 %s 开始跑数据' % current_date)
        while current_date <= date.today():
            url = 'http://www.shfe.com.cn/data/dailydata/kx/kx%s.dat' % current_date.strftime('%Y%m%d')
            logger.info('开始请求 %s' % url)
            resp = requests.get(url, timeout=5)

            if resp.status_code != 200:
                logger.warning('请求返回状态码非 200')
                current_date += timedelta(days=1)
                continue

            try:
                resp = resp.json()
                if not resp:
                    raise Exception('%s 空数据' % current_date)
                df = pd.read_json(json.dumps(resp['o_curinstrument']))
                df = df[['PRODUCTNAME', 'VOLUME', 'DELIVERYMONTH']]
                df = df[~df.PRODUCTNAME.str.contains('计')][~df.DELIVERYMONTH.str.contains('计')]
                df['PRODUCTNAME'] = df['PRODUCTNAME'].apply(lambda i: i.strip())
            except Exception as e:
                logger.error('%s 解析错误 %s' % (current_date, e.args[0]))
                current_date += timedelta(days=1)
                continue

            for metal in set(df['PRODUCTNAME']):
                symbol_str = '%s_连一_VOLUME' % metal

                # symbol 是否存在, 若不存在则新建
                symbol = Symbol.objects.filter(symbol=symbol_str).first()
                if not symbol:
                    logger.info('symbol %s not exist, adding to symbol...' % symbol_str)
                    in_list = list(filter(lambda j: j in metal, varieties_mapping.keys()))
                    symbol = Symbol(
                        title='连一日持仓:%s' % metal,
                        symbol=symbol_str,
                        table_name='data_shfe_day_kline',
                        unit='手',
                        source='SHFE爬虫',
                        duration_unit='d',
                        varieties=varieties_mapping[in_list[0]]
                    )
                    Symbol.objects.bulk_create_all_envs([symbol], logger=logger)

                amount = df[df.PRODUCTNAME == metal].sort_values('DELIVERYMONTH', ascending=True).iloc[0].VOLUME
                DataShfeDayKLine.objects.update_or_create_all_envs(
                    logger=logger,
                    symbol=symbol_str,
                    date=current_date,
                    defaults={'volume': amount}
                )
            current_date += timedelta(days=1)
