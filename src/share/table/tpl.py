# coding: utf-8
import re
import datetime
from collections import ChainMap

from src.share.data import ref_proxy

pattern = r"""
    %(delim)s(?:
      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
      (?P<named>[\w\.]+@?[\w]*)      |   # delimiter and a Python identifier
      {(?P<braced>[\w\.]+@?[\w]*)}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    """


class Template(object):

    delimiter = '$'
    tp = re.compile(pattern % {'delim': re.escape(delimiter)}, re.IGNORECASE | re.VERBOSE)

    def __init__(self, template):
        self.template = template

    @property
    def context(self):
        return {'date': datetime.date.today().strftime('%Y-%m-%d'),
                'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

    def render(self, **kwargs):
        mapping = ChainMap(kwargs, self.context)

        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                if named not in mapping:
                    code = named.split('@')
                    if len(code) == 1:
                        code = code[0]
                        data_type = 'symbol'
                    elif len(code) == 2:
                        code, data_type = code
                    else:
                        raise Exception('string: %s can not render' % named)
                    data = ref_proxy(code, data_type, limit=1, timestamp=False)[0]
                    if isinstance(data, datetime.datetime):
                        data = data.strftime('%Y-%m-%d %H:%M')
                    return str(data)
                else:
                    return str(mapping[named])
            if mo.group('escaped') is not None:
                return self.delimiter
            raise ValueError('Unrecognized named group in pattern',
                             self.tp)

        return self.tp.sub(convert, self.template)
