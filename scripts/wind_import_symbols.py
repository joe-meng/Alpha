# -- coding: utf-8 --
import init

import logging
import pandas as pd

from symbols.models import Symbol


FILE_PATH = '~/desktop'

logger = logging.getLogger(__name__)
df = pd.read_csv(FILE_PATH)
df = df.dropna(thresh=5)
df.index = df['指标名称']
df = df.drop('指标名称', 1)

duration_unit_mapping = {'日': 'd', '周': 'w', '月': 'm', '年': 'y'}
new_symbol_list = []

varieties_mapping = { '强麦': '强麦', '强筋小麦': '强麦', '普麦': '普麦', '硬麦': '普麦', '白小麦': '普麦', '棉花': '棉花', '棉':'棉花', '白糖': '白糖', '白砂糖': '白糖', '甲醇': '甲醇', '玻璃': '玻璃', '油菜籽': '油菜籽', '菜籽粕': '菜粕', '菜粕': '菜粕', '菜籽油': '菜籽油', '粳稻': '粳稻', '早籼稻': '早籼稻', '晚籼稻': '晚籼稻', '动力煤': '动力煤', '铁合金': '铁合金', '锰硅': '锰硅', '硅铁': '硅铁', 'PTA': 'PTA', '玉米': '玉米', '豆油': '豆油', '大豆': '豆油', '豆一': '豆一', '大豆1号': '豆一', '大豆2号': '豆二', '豆二': '豆二', '豆粕': '豆粕', 'PVC': 'PVC', '聚氯乙烯': 'PVC', '焦煤': '焦煤', '聚丙烯': '聚丙烯', '纤维板': '纤维板', '胶合板': '胶合板', '铁矿石': '铁矿石', '鸡蛋': '鸡蛋', '焦炭': '焦炭', '棕榈油': '棕榈油', 'LLDPE': 'LLDPE', '聚乙烯': 'LLDPE', '玉米淀粉': '玉米淀粉', '铜': 'Cu', '铝': 'Al', '铅': 'Pb', '锌': 'Zn', '镍': 'Ni', '锡': 'Sn', '天然橡胶': 'Ru', '燃料油': 'Fu', '黄金': 'Au', '螺纹钢': 'Rb', '线材': 'Wr', '白银':'Ag', '沥青': 'Bu', '热轧卷板': 'Hc', }

for title, row in df.to_dict().items():
    duration_unit = duration_unit_mapping[row['频率']]
    in_list = list(filter(lambda j: j in title, varieties_mapping.keys()))
    s = Symbol(
        title=title,
        duration_unit=duration_unit,
        symbol=row['指标ID'],
        source='wind_%s' % row['来源'],
        updated_at=row['更新时间'],
        unit=row['单位'],
        table_name='data_wind',
        varieties=varieties_mapping[in_list[0]]
    )
    new_symbol_list.append(s)

Symbol.objects.bulk_create_all_envs(
    new_symbol_list,
    logger=logger,
)

