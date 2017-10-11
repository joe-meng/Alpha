#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
import logging

from common.views import BackstageBaseAPIView
from common.utils import log_exception
from com_interface.lib import MapInterfaceObject


logger = logging.getLogger("use_info_ms")


class TypestView(BackstageBaseAPIView, MapInterfaceObject):


    @log_exception
    def get(self, request):
        u"""
        获取所有的分类
        ---


        """

        return self.get_http_res(self.type_res)



