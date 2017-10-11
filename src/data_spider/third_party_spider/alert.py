# -- coding: utf-8 --

import json
import requests
import datetime

from city_weather import MysqlQuery
def main():
    headers = {
        # 'Cookie': 'vjuids=bcc55107.15b0dde4dfe.0.f7edbb862930a; UM_distinctid=15ea7714801225-00a103fdc4ec3-31637e01-13c680-15ea771480292; f_city=%E4%B8%8A%E6%B5%B7%7C101020100%7C; __auc=74ce05e815eb6e5380569e2af26; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1506047773,1506077173,1506331293,1506563000; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1506563843; vjlast=1490586324.1506563000.11',
        'Host': 'product.weather.com.cn',
        'Referer': 'http://www.weather.com.cn/alarm/warninglist1.shtml',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*'
    }
    url = "http://product.weather.com.cn/alarm/grepalarm_cn.php?_=1506566185146"
    more_url = "http://product.weather.com.cn/alarm/webdata/"
    req= requests.get(url, headers=headers)
    req.encoding='utf-8'
    reqtext=req.text
    num = req.text.find('"data":')
    pos = num+8
    area_list=reqtext[pos:-3].split(']')

    for i in range(len(area_list)):
        if area_list[i]:
            url_part = area_list[i].replace('"','').replace('[','')[1:].split(',')[1]
            child_url= more_url + url_part
            response = requests.get(child_url,headers=headers)
            response.encoding='utf-8'
            alert_dict = eval(response.text[14:])
            ALERTID = alert_dict["ALERTID"][18:]
            alert_title = alert_dict["head"]
            alert_pubtime = alert_dict["ISSUETIME"]
            alert_stoptime = alert_dict["RELIEVETIME"]
            alert_url = "http://www.weather.com.cn/alarm/newalarmcontent.shtml?file=%s" % url_part
            alert_province = alert_dict['PROVINCE']

            alert_type =ALERTID[:-2]
            alert_level =ALERTID[-2:]

            value = " '%s','%s','%s','%s' ,'%s','%s' ,'%s' ,'%s' " % ( alert_type,alert_level, alert_title,alert_pubtime,alert_stoptime,alert_url,alert_province,url_part)
            wheres = "part_url ='%s';" % url_part
            kwargs={"column":"id","table":"weather_alert","wheres":wheres}
            data = MysqlQuery("select",**kwargs)
            if data:
                1==1
            else:
                kwargs = {'table':'weather_alert',
                       'column':'alert_type,alert_level,alert_title,alert_pubtime,alert_stoptime,alert_url,alert_province,part_url',
                       'values':value
                       }
                MysqlQuery("insert",**kwargs)

if __name__ == '__main__':
    main()

