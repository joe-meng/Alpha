#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
# from datetime import datetime
import datetime
import time
import math
import when


from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
# from common.utils import gen_page_info
from common.utils import log_exception
from alert.models import Alert
# from django.db import connection


logger = logging.getLogger("use_info_ms")


class AlertRecentDayView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取最近有预警的日期
        ---

        parameters:

        """
        res = {}
        alert_objs = Alert.objects.order_by('-created_at').all()
        obj = alert_objs[0]
        res['recent_day'] = str(obj.created_at)[:10]
        logger.info('正常返回最近有预警的日期')
        return BackstageHTTPResponse(
                data=res,
                message=u'正常返回最近有预警的日期').to_response()



