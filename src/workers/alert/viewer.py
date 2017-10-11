# coding: utf-8
import json
from urllib import request, parse
import datetime
import logging

from share.contrib import get_mysql_client
from workers.share.viewer import Message, MessageViewer
import conf


class AlertMessage(Message):
    """消息类供消息观察者使用"""

    def __init__(self, text):
        super(AlertMessage, self).__init__(text)
        self.json = json.loads(self.text)
        self._subscribers = None

    @property
    def user(self):
        return self.json.get('user') or ''

    @property
    def body(self):
        return self.json['alert']['message']

    @property
    def is_alert(self):
        return self.json['alert']['enable']

    @property
    def formula_id(self):
        return self.json['formula']['id']

    @property
    def variety(self):
        return self.json['chart']['variety']

    @property
    def price(self):
        return self.json['chart']['price']

    @property
    def contract(self):
        return self.json['chart']['contract']

    @property
    def subscribers(self):
        # 获取该消息的所有订阅者
        if self._subscribers is None:
            sql = 'select `id` from varieties_record where code=%s'
            with get_mysql_client() as cursor:
                cursor.execute(sql, (self.variety,))
                result = cursor.fetchone()
            if result:
                varieties_id = result['id']
                sql = ('select a.user_id, c.openid from user_subscription_varieties as a '
                       'left join user_subscription_formula as b on a.varieties_id=b.varieties_id '
                       'left join user as c on a.user_id=c.id where a.varieties_id=%s '
                       'and b.formula_id=%s and a.user_id=b.user_id;')
                with get_mysql_client() as cursor:
                    cursor.execute(sql, (varieties_id, self.formula_id))
                    self._subscribers = cursor.fetchall()
            else:
                self._subscribers = []
        return self._subscribers


class SubscriberViewer(MessageViewer):
    """发送给预警消息订阅者并且去重"""
    now = None
    today = None

    def update(self, msg):
        self.now = datetime.datetime.now()
        today = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
        self.today = today + datetime.timedelta(hours=3) - datetime.timedelta(days=1 + (self.now.hour < 3))
        logging.info('msg subscribers: %s', msg.subscribers)
        for subscriber in msg.subscribers:
            if not self.has_emit(msg, subscriber):
                self.emit(msg, subscriber)

    def has_emit(self, msg, subscriber):
        sql = ('select id from alert_alert where user_id=%s and triggered_by=%s '
               'and variety=%s and price=%s and created_at>=%s;')
        with get_mysql_client() as cursor:
            cursor.execute(sql, (subscriber['user_id'], msg.formula_id,
                                 msg.variety, msg.price,
                                 self.today))
            result = cursor.fetchone()
        return bool(result)

    def emit(self, msg, subscriber):
        # 持久化到数据库
        alert_id = self.save(msg, subscriber)
        # 发送到微信服务号
        if subscriber['openid']:
            self.send(msg, subscriber, alert_id)

    def save(self, msg, subscriber):
        # 持久化到数据库
        sql = ('insert alert_alert set user_id=%s, body=%s, variety=%s, contract=%s, '
               'price=%s, triggered_by=%s, created_at=%s, is_pushed=%s;')
        with get_mysql_client() as cursor:
            cursor.execute(sql, (subscriber['user_id'], msg.body, msg.variety,
                                 msg.contract, msg.price, msg.formula_id, self.now, 1))
            alert_id = cursor.lastrowid
        return alert_id

    def send(self, msg, subscriber, alert_id):
        # 发送到微信服务号
        url = "%s/#/?id=%s" % (conf.http.get('host'), alert_id)
        redirect_uri = '%s?url=%s' % (conf.WECHAT_AUTH_URL, url)
        redirect_uri = parse.quote(redirect_uri)
        auth_url = ('https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&'
                    'redirect_uri={uri}&response_type=code&scope=snsapi_userinfo&'
                    'agentid=AGENTID&state=STATE&connect_redirect=1#wechat_redirect').format(appid=conf.WECHAT_APPID,
                                                                                             uri=redirect_uri)
        now_str = self.now.strftime('%Y-%m-%d %H:%M')
        data = {'appId': conf.WECHAT_APPID,
                'messages': [{'key': 'first', 'tplData': {'value': 'alpha预警'}},
                             {'key': 'keyword1', 'tplData': {'value': '行情预警'}},
                             {'key': 'keyword2', 'tplData': {'value': msg.body}},
                             {'key': 'keyword3', 'tplData': {'value': now_str}},
                             {'key': 'remark', 'tplData': {'value': ''}}],
                'openId': subscriber['openid'],
                'templateId': conf.template_id,
                'url': auth_url}
        logging.info("微信发送data: %s", data)
        headers = {'Content-Type': 'application/json'}
        req = request.Request(conf.WECHAT_SEND_TEMPLATE_MSG_URL,
                              json.dumps(data).encode('utf-8'),
                              headers)
        resp = request.urlopen(req)
        result = resp.read()
        logging.info('发送微信模板消息成功:%s' % result)


class QueueViewer(MessageViewer):
    """发送到队列"""
    pass


class ShortMessageViewer(MessageViewer):
    """发送到手机短信"""

    def update(self, msg):
        pass
