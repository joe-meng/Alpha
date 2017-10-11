# -- coding: utf-8 --
from datetime import datetime, date
import re
import logging
from lxml import html
import pymysql
import requests
import datetime

def MysqlQuery(q_dml,**kwargs):
    config = {
          'host':'172.16.88.140',
          'port':20306,
          'user':'exingcai',
          'password':'uscj!@#',
          'db':'alpha',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }
    db = pymysql.connect(**config)
    cursor = db.cursor()

    if q_dml == 'select':
        cursor.execute("select %s from %s where %s ;" % (kwargs['column'],kwargs['table'],kwargs['wheres']  ))
        data = cursor.fetchall()
        return data
    else:
        sql = "%s into %s (%s ) select %s ;" % (q_dml,kwargs['table'],kwargs['column'],kwargs['values'])
        try:
            #执行sql
            cursor.execute(sql)
            db.commit()
        except:
            #发生错误时回滚
            db.rollback()
    db.close()



logger = logging.getLogger(__name__)



def last_date(day_num):
    """
    计算后几天的日期
    """
    now_time = datetime.datetime.now()
    date = []
    for i in range(day_num):
        time = now_time + datetime.timedelta(days=i)
        date.append(time)
        date[i] = date[i].strftime('%Y-%m-%d')
    return date



def city_weather():

    date = last_date(15)
    source = "2345天气预报"
    kwargs = {'column':'code','table':'area_info','wheres':'code>100 '}
    citycode = MysqlQuery('select',**kwargs)
    for i in range(len(citycode)):

        url = "http://tianqi.2345.com/t/q.php?id=%s " % citycode[i]['code']
        url_air = "http://tianqi.2345.com/air-%s.htm" % citycode[i]['code']
        logger.info('开始爬取 %s, url: %s ,%s' % (source, url ,url_air))
        print(url,url_air)

        response = requests.get(url, timeout=10)
        response_air = requests.get(url_air, timeout=10)
        dom = html.fromstring(response.text)
        dom_air = html.fromstring(response_air.text)
        w_info = dom.xpath('//div[@class="wea-detail"]//b/text()')
        tem_low = dom.xpath('//div[@class="wea-detail"]//i/font[@class="blue"]/text()')
        tem_high = dom.xpath('//div[@class="wea-detail"]//i/font[@class="red"]/text()')
        wind_line = dom.xpath('//div[@class="wea-detail"]//i/text()[position()=2]')
        humidity = dom.xpath('//div[@class="unit-1"]//ul/li[position()=2]/i/text()')
        aqi_level = dom_air.xpath('//div[@class="bmeta"]//dl//i/text()')
        aqi_num = dom_air.xpath('//div[@class="bmeta"]//div[@class="td td3 tc"]/span/text()')

        for j in range(len(w_info)):
            wind ,wind_level = wind_line[j].split('风',1)
            wind = wind.replace("\n", "") +'风'
            tem_high[j] = tem_high[j].replace('℃','')
            wind_level=wind_level.replace(" ","").replace("级","")
            humidity.append('')

            if aqi_level:
                1==1
            else:
                aqi_level=['','','','','','','','','','','','','','','']
                aqi_num=['','','','','','','','','','','','','','','']

            if wind_level.find('-')==-1:
                wind_high , wind_low =wind_level ,wind_level

            else:
                wind_low,wind_high = wind_level.split('-')

            value="%s,'%s', '%s' , '%s' ,'%s' ,'%s' ,'%s' ,'%s' ,'%s','%s','%s',now()" %(citycode[i]['code'],w_info[j] , tem_high[j],tem_low[j], wind ,wind_high ,wind_low ,humidity[j],aqi_level[j],aqi_num[j],date[j])

            kwargs = {'table':'weather_base',
            'column':'`code`,`desc`,tem_high,tem_low,wind,wind_high,wind_low,humidity,aqi_level,aqi_num,date_time,update_time',
            'values': value }
            MysqlQuery('replace',**kwargs)



