import json

import logging
from datetime import datetime

import re
from django.db import models

from enums import TableTypes
from model_mixins import CreatedAtMixin, AlphaBaseMixin, UpdatedAtMixin
from share.data import TableData

logger = logging.getLogger(__name__)

REGISTERED_FUNCS = ('datetime',)


class Tables(CreatedAtMixin, UpdatedAtMixin, AlphaBaseMixin):
    """
    self.content: 表格格式，以 {"location": "A1:B2", "value": "xxx"} 组成的 list
    self._content: python 格式的数据，可以是填充或未填充数据的
    self._filled: 是否已填充
    self._filled_at: 填充时间
    """
    name = models.CharField('名称', null=True, max_length=128)
    description = models.CharField('描述', null=True, max_length=256)
    type = models.SmallIntegerField('表格种类', choices=TableTypes.choices())
    content = models.TextField('内容', default='[]')

    class Meta:
        db_table = 'tables'
        ordering = ['-id']

    def __init__(self, *args, **kwargs):
        self._filled = False
        self._filled_at = None
        super(Tables, self).__init__(*args, **kwargs)
        self._content = json.loads(self.content)
        self.fill_in_contents()

    def refresh_from_db(self, using=None, fields=None):
        super(Tables, self).refresh_from_db(using=using, fields=fields)
        self._content = json.loads(self.content)
        self.fill_in_contents()

    def fill_in_contents(self):
        """
        为 ==symbol.column.attribute 装载数据
        """
        if self._filled:
            return

        if self.type == TableTypes.LOCATION.value:
            for item in self._content:
                if item['value'].startswith('=='):
                    if item['value'].endswith('.latest'):
                        value_list = TableData(item['value'][2:-7], 'symbol', limit=1, desc=True).get_list()
                        value = value_list[-1] if value_list else None
                        item['value'] = value
        self._filled = True
        self._filled_at = datetime.now()

    def parse_symbol_str(self, symbol):
        TableData(symbol, 'symbol', limit=1, desc=True).get_list()

    def validate_location(self, location):
        """
        location 是 A1 或 A1:B2 格式
        """
        return bool(re.match(r'([A-Z]+[0-9]+)((?:\:)([A-Z]+[0-9]+))?', location))

    def validate_value(self, value):
        """
        value 是 string | int | float 格式
        ==symbol.column.attribute 表示数据源是 symbol
        =datetime(xxx,fmt_str) 表示 datetime
        # =SUM(A1:A10) 预留给公式，未实现
        string 表示数据源是 str
        int 表示数据源是 int
        float 表示数据源是 float
        """
        check_list = []
        check_list.append(isinstance(value, (str, int, float)))
        if isinstance(value, str):
            if value.startswith('=='):
                try:
                    self.parse_symbol_str(value[2:])
                    symbol_check_passed = True
                except Exception as e:
                    symbol_check_passed = False
                check_list.append(symbol_check_passed)
            elif value.startswith('='):
                func_check_passed = False
                func_string = value[1:]
                func_matched = re.match(r'^([^(]*)', func_string)
                if func_matched in REGISTERED_FUNCS:
                    # TODO: 检查参数
                    func_check_passed = True
                check_list.append(func_check_passed)
        return all(check_list)

    def validate_locations(self, content):
        try:
            assert all([self.validate_location(i['location']) for i in content])
        except Exception as e:
            logger.info('%s 的 location 校验失败: %s' % (self.id, e.args))
            return False
        return True

    def validate_values(self, content):
        try:
            assert all([self.validate_value(i['value']) for i in content])
        except Exception as e:
            logger.info('%s 的 value 校验失败' % self.id)
            return False
        return True

    def validate_content(self, content=None):
        try:
            content = json.loads(content or self.content)
            assert isinstance(content, list)
            assert all([isinstance(i, dict) and 'location' in i and 'value' in i for i in content])
            assert self.validate_locations(content)
            assert self.validate_values(content)
        except Exception as e:
            logger.warning('%s validate failed: %s' % (self.id, e.args))
            return False
        return True
