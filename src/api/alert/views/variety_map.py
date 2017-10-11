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
from django.db import connection


logger = logging.getLogger("use_info_ms")


class AlertVarietiesView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取品类对应关系
        ---

        parameters:


        """
        res = {}
        with connection.cursor() as cursor:
            # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
            cursor.execute("SELECT code, long_name FROM varieties")
            row = cursor.fetchall()
            for vals in row:
                res[str(vals[0]).lower()] = vals[1]

        logger.info('正常返回品类对应关系')
        return BackstageHTTPResponse(
                data=res,
                message=u'正常返回品类对应关系').to_response()



