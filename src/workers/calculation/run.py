#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *
from server import SyncCalcServer

if __name__ == '__main__':
    logger.info("计算公式模块启动")
    SyncCalcServer().run()
    logger.info("计算公式模块结束")

