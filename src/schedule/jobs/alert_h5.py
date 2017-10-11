# coding: utf-8

from datetime import datetime
# import pandas as pd
# import numpy as np
import sys
import os

new_path_list = os.path.abspath(__file__).split(os.sep)
while True:
    if new_path_list[-1] == 'src':
        break
    else:
        new_path_list = new_path_list[:-1]


new_lib_path = os.sep.join(new_path_list+['workers', 'calculation'])
sys.path.append(new_lib_path)
sys.path.append(os.sep.join(new_path_list))


from share.contrib import get_mysql_client
from share.data.ship import ref_ship
from workers.calculation.lib.mathlib import data_gap
from schedule.scheduler import get_scheduler


scheduler = get_scheduler()

def cal_partical_man_number(varieties_id):
    """每天算出各个品种的参与人数"""
    with get_mysql_client() as cr:
        sql="""
        select user_id, id
        from alert_prediction_record
        where varieties_id = '%s'
        group by user_id
        """%varieties_id
        cr.execute(sql)
        res = cr.fetchall()

        sql1 = """
                update alert_ai_varieties set count_user = '%s' where id = '%s'
        """ % (len(res), varieties_id)
        cr.execute(sql1)
        return True


def insert_quotes_vals(varieties_name, varieties_id):
    """每天按工作日插入明天竞猜行情信息"""
    today = str(datetime.now())[:10]
    with get_mysql_client() as cr:
        # 查询下个工作日的sql
        sql1 = "select settlement_date from main_contract where settlement_date > '%s' and varieties='%s' order by settlement_date"%(today, varieties_name)

        cr.execute(sql1)
        vals = cr.fetchone()
        if vals:
            next_work_day = vals.get('settlement_date')
            # 插入下个工作日
            cr.execute("select id from alert_quotes_record where date = '%s' and varieties_id = '%s' " %(next_work_day, varieties_id))
            vals_lst = cr.fetchall()
            if len(vals_lst) == 1:
                return
            elif len(vals_lst) > 1:
                # 删除多余记录
                # delete_lst = []
                for i in range(len(vals_lst)-1):
                    # delete_lst.append(i)
                    cr.execute("delete from alert_quotes_record where id = %s "%vals_lst[i]['id'])
            else:
                # 插入新记录
                sql2 = """
                    INSERT INTO `alpha`.`alert_quotes_record`
                                (`price`, `date`, `created_at`, `updated_at`, `varieties_id`)
                         VALUES ('0', '%s', '%s', '%s', '%s')
                """%(next_work_day, str(datetime.now())[:19], str(datetime.now())[:19], varieties_id)
                cr.execute(sql2)
        return


def cal_win_percent(date):
    """每天计算胜率，胜负次数，参与次数"""
    with get_mysql_client() as cr:
        sql = """
                select IFNULL(t2.fail_number, 0) as fail_number, t1.user_id,  IFNULL(t1.victor_number, 0) as victor_number
                from
                    (select count(*) as victor_number, user_id
                    from alert_prediction_record
                    where is_true = 't' and if_visible = '1'
                    group by user_id) as t1
                left outer join
                    (select count(*) as fail_number, user_id
                    from alert_prediction_record
                    where is_true = 'f' and if_visible = '1'
                    group by user_id) as t2
                    on t1.user_id = t2.user_id
            UNION
                select IFNULL(t4.fail_number, 0) as fail_number, t4.user_id,  IFNULL(t3.victor_number, 0) as victor_number
                from
                    (select count(*) as victor_number, user_id
                    from alert_prediction_record
                    where is_true = 't' and if_visible = '1'
                    group by user_id) as t3
                right outer join
                    (select count(*) as fail_number, user_id
                    from alert_prediction_record
                    where  is_true = 'f' and if_visible = '1'
                    group by user_id) as t4
                    on t3.user_id = t4.user_id
        """
        cr.execute(sql)
        head = cr.description
        vals_lst = cr.fetchall()
        for vals in vals_lst:
            vals['part_number'] = vals['victor_number'] + vals['fail_number']
            vals['win_percent'] = round(float(vals['victor_number']) / float((vals['victor_number']+vals['fail_number'])), 4)
            sql2 = """update user
                        set victor_number = '%(victor_number)s',
                            part_number = '%(part_number)s',
                            fail_number = '%(fail_number)s',
                            win_percent = '%(win_percent)s'
                        where id = '%(user_id)s'""" % vals
            cr.execute(sql2)
    return True


def judgment(varieties_name, varieties_id, date):
    """判断竞猜的正确与否,并写入数据库"""
    end_day = datetime.strptime(date, '%Y-%m-%d')
    data = ref_ship(varieties_name, 'SETTLE', limit=2, end=end_day)

    prediction = 'up'
    if data[0] < data[1]:
        prediction = 'down'

    with get_mysql_client() as cr:
        sql = """
            select id, prediction
            from alert_prediction_record
            where varieties_id = '%s' and date = '%s'
        """%(varieties_id, date)
        cr.execute(sql)
        lst = cr.fetchall()
        for vals in lst:
            if vals['prediction'] == prediction:
                cr.execute("update alert_prediction_record set is_true = 't' where id = '%s'"%vals['id'])
            else:
                cr.execute("update alert_prediction_record set is_true = 'f' where id = '%s'" % vals['id'])
    return


def get_quotes(varieties, date):
    """获取行情数据"""
    # price = ''
    res = {}
    price = 'SETTLE'
    day = datetime.strptime(date, '%Y-%m-%d')
    data = ref_ship(varieties, price, limit=2, start=day, end=day)
    if data:
        data = ref_ship(varieties, price, limit=2, end=day)
        d1, d2, gd, rate = data_gap(data)
        res['price'] = data[0]
        if gd[0] < 0:
            res['trend'] = 'up'
        elif gd[0] > 0:
            res['trend'] = 'down'
        else:
            res['trend'] = 'c'
        res['change_price'] = abs(round(gd[0], 4))
        res['change_percent'] = abs(round(rate[0], 4))
        # res['yes_price'] = data[1]
    return res


def update_quotes(varieties_name, varieties_id, date):
    """把今天结算后的价格信息更新到数据库"""
    res = get_quotes(varieties_name, date)
    res['varieties_id'] =varieties_id
    res['date'] =date
    with get_mysql_client() as cr:
        sql = """
                update alert_quotes_record
                set price = '%(price)s',
                    trend = '%(trend)s',
                    change_price = '%(change_price)s',
                    change_percent = '%(change_percent)s'
                where varieties_id = '%(varieties_id)s' and
                      date = '%(date)s'
        """ % res
        cr.execute(sql)
    return


def start():
    lst = []
    date = None
    with get_mysql_client() as cr:
        sql = """
                select date
                from alert_prediction_record
                order by date desc
        """
        cr.execute(sql)
        vals = cr.fetchone()
        date = str(vals.get('date', None))[:10]

        sql1 = """
            select id, varieties from alert_ai_varieties
        """
        cr.execute(sql1)
        lst = cr.fetchall()
        cal_ranking()
    for varieties_vals in lst:
        varieties_name, varieties_id = varieties_vals.get('varieties'), varieties_vals.get('id')
        judgment(varieties_name, varieties_id, date)
        update_quotes(varieties_name, varieties_id, date)
        cal_win_percent(date)
        insert_quotes_vals(varieties_name, varieties_id)
        cal_partical_man_number(varieties_id)


@scheduler.scheduled_job('cron', hour=17, minute=30)
def cal_ranking():
    """按胜率计算排名"""
    with get_mysql_client() as cr:
        sql = """
            select id, win_percent
            from user
            where part_number != '0'
            order by win_percent desc, part_number desc
        """
        cr.execute(sql)
        lst = cr.fetchall()
        id_lst = []
        ranking = 1
        # percent_lst = []
        for vals in lst:
            user_id = vals['id']
            sql1 = """update user set ranking = '%s' where id = '%s' """ % (ranking, user_id)
            cr.execute(sql1)
            ranking = ranking+1
    return


if __name__ == '__main__':
    start()