#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-07-20

@author: Devin
"""
import datetime

from dateutil import relativedelta


def begin_month(dt=datetime.date.today(), months=0):
    return dt + relativedelta.relativedelta(months=months, day=1)


def next_day(dt=datetime.date.today(), days=1):
    return dt + relativedelta.relativedelta(days=days)


def end_month(dt=datetime.date.today(), months=0):
    return next_day(begin_month(dt, months + 1), -1)


def all_month_end(start_date, end_date):
    month_end = []

    i = 0
    while start_date <= end_month(start_date, i) <= end_date:
        month_end.append(end_month(start_date, i))
        i += 1
    return month_end


def timestamp2datetime(timestamp, convert_to_local=True):
    """
    Converts UNIX timestamp to a datetime object.
    :param timestamp:
    :param convert_to_local:
    :return:
    """
    if isinstance(timestamp, (int, float)):
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        if convert_to_local:  # 是否转化为本地时间
            dt = dt + datetime.timedelta(hours=8)  # 中国默认时区
        return dt
    return timestamp


def begin_year(dt=datetime.date.today(), years=0):
    return dt + relativedelta.relativedelta(years=years, month=1, day=1)


def year_days_remain(dt=datetime.date.today()):
    next_year = begin_year(dt, years=1)
    return(next_year - dt).days

if __name__ == "__main__":
    # today = datetime.date.today()
    # start_date = today + relativedelta.relativedelta(months=-5)
    # print(all_month_end(start_date, today))
    # print(timestamp2datetime(1502789515.684))
    print(year_days_remain())
