#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime


from workers.calculation.lib.mathlib import *

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import log_exception
from alert.models import AiVarieties
from django.db import connection
from share.data import ref_ship
from ..view_lib import get_quotes
from ..models import DayKline

logger = logging.getLogger("use_info_ms")


class QuotesView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取实时最新行情
        ---
        parameters:
            - name: varieties_id
              description: 品类id
              paramType: query
              required: True
        """
        today = datetime.datetime.today()
        date = str(today)[:10]
        query_dict = request.query_params.dict().copy()
        varieties_id = query_dict.get('varieties_id', None)
        if not varieties_id:
            return BackstageHTTPResponse(
                                BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                message=u'品类id必填').to_response()
        var_obj = AiVarieties.objects.get(pk=varieties_id)
        varieties = var_obj.varieties
        res = get_quotes(varieties, date)
        high = ref_ship(varieties, 'HIGH', limit=2, start=today, end=today)
        low = ref_ship(varieties, 'LOW', limit=2, start=today, end=today)
        open = ref_ship(varieties, 'OPEN', limit=2, start=today, end=today)
        opi = ref_ship(varieties, 'OPI', limit=2, start=today, end=today)
        vol = ref_ship(varieties, 'VOL', limit=2, start=today, end=today)
        dk_objs = DayKline.objects.filter(contract=varieties+'9999', date_time=date+' 00:00:00').all()
        if dk_objs:
            obj = dk_objs[0]
            if obj.settlement_price:
                res['settlement_price'] = obj.settlement_price
                res['price'] = obj.price_close
            else:
                res['settlement_price'] = None
        res['varieties'] = varieties
        res['high'] = high and high[0] or None
        res['low'] = low and low[0] or None
        res['open'] = open and open[0] or None
        res['opi'] = opi and opi[0] or None
        res['vol'] = vol and vol[0] or None

        logger.info('正常返回品类对应关系')
        return BackstageHTTPResponse(
                data=res,
                message=u'正常返回品类对应关系').to_response()



