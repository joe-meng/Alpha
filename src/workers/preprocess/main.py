# -- coding: utf-8 --
import os
import logs
import logging
import sys
sys.path.append("../..")

from share.mq import channel
from receive_ctp_message import get_info_from_ctp_queue

_logger = logging.getLogger(__name__)

def main():
    get_info_from_ctp_queue()

if __name__ == '__main__':
    # 从ctp获取数据
    _logger.info('start preprocess')
    main()
