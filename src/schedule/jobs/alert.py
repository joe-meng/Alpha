# coding: utf-8
import logging
import datetime
import json
from urllib import request, parse
from sqlbuilder.smartsql import Result, Q, T
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

import conf
from schedule.scheduler import get_scheduler
from share.contrib import get_mysql_client

scheduler = get_scheduler()


def send_alert_history(data):
    # 发送到微信服务号
    logging.info("微信发送data: %s", data)
    headers = {'Content-Type': 'application/json'}
    req = request.Request(conf.WECHAT_SEND_TEMPLATE_MSG_URL,
                          json.dumps(data).encode('utf-8'),
                          headers)
    resp = request.urlopen(req)
    result = resp.read()
    logging.info('发送微信模板消息成功:%s' % result)


@scheduler.scheduled_job('cron', hour=18, minute=30)
def alert_history():
    # 第一次提示当日预警汇总
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    alert_table = T('alert_alert')
    user_table = T('user')
    q = Q(alert_table, result=Result(compile=mysql_compile))
    q = q.tables(q.tables() + user_table).on(alert_table['user_id'] == user_table['id'])
    q = q.fields(alert_table['id'].count().as_('count_value'), user_table['openid'], user_table['id'])
    q = q.group_by(alert_table['user_id'])
    q = q.where(alert_table['created_at'] >= datetime.date.today())
    sql, params = q.select()
    logging.info('sql: %s, params: %s', sql, params)
    with get_mysql_client() as cursor:
        cursor.execute(sql, params)
        result = cursor.fetchall()
    logging.info('result: %s', result)
    for item in result:
        if item['count_value'] and item['openid']:
            q = Q(alert_table, result=Result(compile=mysql_compile))
            q = q.fields(alert_table['body'])
            q = q.where((alert_table['created_at'] >= datetime.date.today())
                        & (alert_table['user_id'] == item['id']))
            q = q.order_by(alert_table['id'])
            q = q.limit(3)
            sql, params = q.select()
            with get_mysql_client() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
            msg = '\n'.join([d['body'] for d in result])
            url = "%s/#/history" % conf.http.get('host')
            redirect_uri = '%s?url=%s' % (conf.WECHAT_AUTH_URL, url)
            redirect_uri = parse.quote(redirect_uri)
            auth_url = ('https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&'
                        'redirect_uri={uri}&response_type=code&scope=snsapi_userinfo&'
                        'agentid=AGENTID&state=STATE&connect_redirect=1#wechat_redirect').format(
                appid=conf.WECHAT_APPID,
                uri=redirect_uri)
            data = {'appId': conf.WECHAT_APPID,
                    'messages': [{'key': 'first', 'tplData': {'value': 'alpha预警'}},
                                 {'key': 'keyword1', 'tplData': {'value': '行情预警'}},
                                 {'key': 'keyword2', 'tplData': {'value': msg}},
                                 {'key': 'keyword3', 'tplData': {'value': now_str}},
                                 {'key': 'remark', 'tplData': {'value': ''}}],
                    'openId': item['openid'],
                    'templateId': conf.template_id,
                    'url': auth_url}
            send_alert_history(data)


@scheduler.scheduled_job('cron', hour=22, minute=30)
def alert_history_compensate():
    # 第二次提示当日预警汇总
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    alert_table = T('alert_alert')
    user_table = T('user')
    q = Q(alert_table, result=Result(compile=mysql_compile))
    q = q.tables(q.tables() + user_table).on(alert_table['user_id'] == user_table['id'])
    q = q.fields(alert_table['id'].count().as_('count_value'), user_table['openid'], user_table['id'])
    q = q.group_by(alert_table['user_id'])
    q = q.where(alert_table['created_at'] > datetime.date.today() + datetime.timedelta(hours=16))
    sql, params = q.select()
    logging.info('sql: %s, params: %s', sql, params)
    with get_mysql_client() as cursor:
        cursor.execute(sql, params)
        result = cursor.fetchall()
    logging.info('result: %s', result)
    for item in result:
        if item['count_value'] and item['openid']:
            q = Q(alert_table, result=Result(compile=mysql_compile))
            q = q.fields(alert_table['body'])
            q = q.where((alert_table['created_at'] >= datetime.date.today())
                        & (alert_table['user_id'] == item['id']))
            q = q.order_by(alert_table['id'])
            q = q.limit(2)
            sql, params = q.select()
            with get_mysql_client() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
            msg = '\n'.join([d['body'] for d in result])
            url = "%s/#/history" % conf.http.get('host')
            redirect_uri = '%s?url=%s' % (conf.WECHAT_AUTH_URL, url)
            redirect_uri = parse.quote(redirect_uri)
            auth_url = ('https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&'
                        'redirect_uri={uri}&response_type=code&scope=snsapi_userinfo&'
                        'agentid=AGENTID&state=STATE&connect_redirect=1#wechat_redirect').format(
                appid=conf.WECHAT_APPID,
                uri=redirect_uri)
            data = {'appId': conf.WECHAT_APPID,
                    'messages': [{'key': 'first', 'tplData': {'value': 'alpha预警'}},
                                 {'key': 'keyword1', 'tplData': {'value': '行情预警'}},
                                 {'key': 'keyword2', 'tplData': {'value': msg}},
                                 {'key': 'keyword3', 'tplData': {'value': now_str}},
                                 {'key': 'remark', 'tplData': {'value': ''}}],
                    'openId': item['openid'],
                    'templateId': conf.template_id,
                    'url': auth_url}
            send_alert_history(data)
