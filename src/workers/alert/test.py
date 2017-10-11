# coding: utf-8
import json
import random
import pika
import datetime
import random
from conf import consumer_conf
from share.contrib import get_mysql_client


def pub():
    # user = (None, '18268174851')
    user = ('', )
    is_alert = (True, )
    formula_id = (4, )
    message = ('【有色在线】铜南储库存日内减少2%，历史上70%的情况造成行情下跌，请注意。', '【有色在线】铜1708合约出现十字星，历史上90%的情况造成行情回撤，请注意。')
    variety = 'cu'
    price = 'WARRANT'
    body = {'user': random.choice(user),
            'is_alert': random.choice(is_alert),
            'formula_id': random.choice(formula_id),
            'message': random.choice(message),
            'variety': variety,
            'price': price}
    body = json.dumps(body)
    connection = pika.BlockingConnection(pika.ConnectionParameters(consumer_conf.host))
    channel = connection.channel()
    channel.exchange_declare(consumer_conf.exchange, type='topic')
    channel.queue_declare(consumer_conf.queue)
    print(body)
    channel.basic_publish(exchange=consumer_conf.exchange,
                          routing_key=consumer_conf.routing_key,
                          body=body)


def test():
    sql = 'select * from chart_sidebar'
    with get_mysql_client() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    for row in result:
        exchange = row['exchange']
        variety = row['variety']
        sidebar = row['sidebar']
        title = row['sidebar_name']
        p_axis = row['p_axis']
        s_axis = row['s_axis']
        size = 1
        graph = 1
        compare = 1

        sql = 'select id from chart_sidebar_copy where exchange=%s and variety=%s and name=%s'
        with get_mysql_client() as cursor:
            cursor.execute(sql, (exchange, variety, title if row['panorama'] == 0 else '全景图'))
            sidebar_id = cursor.fetchone()['id']

        if sidebar == 'panorama_3':
            compare = 2
        elif sidebar == 'panorama_4':
            compare = 3
        else:
            compare = 1

        if row['panorama'] == 1:
            size = 1
        else:
            size = 2

        if sidebar == 'panorama_7':
            graph = 2
        else:
            graph = 1

        sql = 'insert into chart_chart set title=%s, size=%s, graph=%s, compare=%s, p_axis=%s, s_axis=%s'
        with get_mysql_client() as cursor:
            cursor.execute(sql, (title, size, graph, compare, p_axis, s_axis))
            chart_id = cursor.lastrowid

        sql = 'insert into chart_sidebar_chart set chart_id=%s, sidebar_id=%s'
        with get_mysql_client() as cursor:
            cursor.execute(sql, (chart_id, sidebar_id))

        sql = 'update chart_line set chart_id=%s where exchange=%s and variety=%s and sidebar=%s'
        with get_mysql_client() as cursor:
            cursor.execute(sql, (chart_id, exchange, variety, sidebar))
    print('done')


def sidebar():

    sql = 'select distinct(variety) from chart_sidebar'
    with get_mysql_client() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    for row in result:
        variety = row['variety']
        sql = 'insert into chart_sidebar_copy set exchange=%s, variety=%s, name=%s'
        with get_mysql_client() as cursor:
            cursor.execute(sql, ('', variety, '全景图'))
    sql = 'select * from chart_sidebar where panorama=0'
    with get_mysql_client() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    for row in result:
        exchange = row['exchange']
        variety = row['variety']
        name = row['sidebar_name']
        sql = 'insert into chart_sidebar_copy set exchange=%s, variety=%s, name=%s'
        with get_mysql_client() as cursor:
            cursor.execute(sql, (exchange, variety, name))


def math():
    import pprint
    from src.share.data import ProxyData
    data_code = 'symbol(S0033227) / 0.97 - ((((symbol(S0174655) / 0.615 * 0.62 / 0.92) * 0.9 + (symbol(S0167818) / 0.66 * 0.62) * 0.1) * 1.6 + symbol(S5120141) * 0.5) / 0.9 * 0.96 / 0.82 + 120)'
    obj = ProxyData(data_code, 'math')
    data = obj.get_list()
    pprint.pprint(data)


if __name__ == '__main__':
    # test()
    # sidebar()
    math()
