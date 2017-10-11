# -*- coding: utf-8 -*-
import logging
from datetime import date, datetime

import re
import requests

from lxml import html

from s_common import Spider
from third_party_data.models import LGMIData


def parse_text(body):
    """
    唐山象屿正丰总库存, 钢胚库存, 总入库量, 钢胚入库量, 总出库量, 钢胚出库量
    :param body:
    :return:
    """
    try:
        matched_values = \
        re.findall(r'唐山象屿正丰总库存(.*)万吨，其中钢坯库存(.*)万吨。.*总入库量为(.*)万吨，其中钢坯(.*)万吨，总出库量(.*)万吨，其中钢坯(.*)万吨。', body)[0]
    except:
        raise Exception('解析失败, body: %s' % body)

    return {
        '唐山象屿正丰总库存': {
            'amount': matched_values[0],
            'symbol': 'LGMI0000',
        },
        '钢胚库存': {
            'amount': matched_values[1],
            'symbol': 'LGMI0001',
        },
        '总入库量': {
            'amount': matched_values[2],
            'symbol': 'LGMI0002',
        },
        '钢胚入库量': {
            'amount': matched_values[3],
            'symbol': 'LGMI0003',
        },
        '总出库量': {
            'amount': matched_values[4],
            'symbol': 'LGMI0004',
        },
        '钢胚出库量': {
            'amount': matched_values[5],
            'symbol': 'LGMI0005',
        },
    }


logger = logging.getLogger(__name__)


class LGMISpider(Spider):
    """
    兰格钢铁数据 LGMI
    http://luliao.lgmi.com/list_info.aspx?thepage=1&pColumncode=BBG&pArticleCode=B21&
    """

    def _run(self):
        url = 'http://luliao.lgmi.com/list_info.aspx?thepage=1&pColumncode=BBG&pArticleCode=B21&'
        logger.info('开始请求列表页 %s' % url)
        resp = requests.get(url, timeout=5)
        dom = html.fromstring(resp.text)
        links = dom.xpath('//ul/li/a[contains(text(), "%s")]' % '象屿正丰库存')
        days = [
            datetime.strptime('%s-%s' % (
                date.today().year,
                link.xpath('following-sibling::div/text()')[0].strip('[]').replace('.', '-')
            ), '%Y-%m-%d').date() for link in links
        ]

        for (link, day) in zip(links, days):
            exist = LGMIData.objects.filter(date=day).first()
            if exist:
                logger.info('%s 已在数据库，跳过' % day)
                continue

            detail_page_url = link.xpath('@href')[0]
            logger.info('开始请求详情页 %s' % detail_page_url)
            detail_page_resp = requests.get(detail_page_url, timeout=5)
            if len(detail_page_resp.content) <= 300:
                logger.error('详情页要求登录 %s' % detail_page_url)
                continue
            detail_page_dom = html.fromstring(detail_page_resp.content.decode('gbk'))
            body = detail_page_dom.xpath('//div[@class="t3"]/text()')[1].strip()
            try:
                parsed_dict = parse_text(body)
            except Exception as e:
                continue
            for title, item in parsed_dict.items():
                LGMIData.objects.update_or_create_all_envs(
                    logger,
                    symbol=item['symbol'],
                    date=day,
                    defaults={
                        'amount': item['amount']
                    }
                )
