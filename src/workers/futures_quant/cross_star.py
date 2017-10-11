# -*- coding: utf-8 -*-
from __future__ import division

import datetime
from read_alpha import *




def  cross_star_history(dataset):
    '''
    cross_star_history
    '''
    now = datetime.datetime.now()
    insert_date = now.strftime("%Y-%m-%d %H:%M:%S")


    open_close = abs(dataset['price_open']-dataset['price_close'])
    cross_close = dataset['price_close']
    ratio_list= []
    for i in dataset.index:
        if cross_close[i] !=0:
            ratio_list.append(round(open_close[i]/cross_close[i],5))

    history_data = pd.DataFrame()
    history_data['date'] = dataset['date_time']
    history_data['varieties'] = dataset['varieties']
    history_data['contract'] = dataset['contract']
    history_data['ratio'] = ratio_list
    history_data['insert_date'] = insert_date
    return history_data


def cross_sign(dataset,ratio):
    '''
    返回十字星索引位置
    '''

    open_close = abs(dataset['price_open']-dataset['price_close'])
    cross_close = dataset['price_close']
    cross_date = []
    index = []
    for i in dataset.index:
        if cross_close[i] !=0 and open_close[i]/cross_close[i] <= ratio:
            if i not in index:
                index.append(i)
                cross_date.append(dataset['date_time'][i])
    return index,cross_date


def get_kline_ud(dataset,index):
    '''
    输出十字星出现后,下个工作日开盘价和收盘价都上涨/下跌的概率
    返回十字星出现后,下个工作日开盘价和收盘价都上涨/下跌的位置
    '''
    up = 0
    down = 0
    up_index = []
    down_index = []
    if len(index) !=0:
        for i in index:
            cross_open = dataset['price_open'][i]
            cross_close = dataset['price_close'][i]
            if i+1  in dataset.index:
                next_open = dataset['price_open'][i+1]
                next_close = dataset['price_close'][i+1]
            else: continue
            if max(cross_open,cross_close) < min(next_open,next_close): #
                up += 1
                up_index.append(i)
            elif min(cross_open,cross_close) > max(next_open,next_close):
                down+=1
                down_index.append(i)
        # print '下个工作日的K线收盘价、开盘价高于/低于十字星的样本数:',up+down
        # print "下个工作日的K线收盘价、开盘价高于/低于十字星的概率:",round((up+down)/len(index),4)
    return up_index,down_index


def get_kline_rise(dataset,index):

    up = 0
    rise_index = []

    if len(index) != 0:
        rise= np.array(dataset['rise'])
        rise.sort()
        rise1 = rise[rise>0] #涨幅大于0
        rise2 = rise[rise<0] #涨幅小于0


        for i in index:
            if i+1 in dataset.index:
                next_rise = dataset['rise'][i+1]
            else:continue
            if  next_rise > rise1[int(len(rise1)*2/10)] or next_rise < rise2[int(len(rise2)*8/10)]:
                up += 1
                rise_index.append(i)
        # print '涨幅显著的样本数:',len(rise_index)
        # print '涨幅显著的比率:',round(up/len(index),4)

    return rise_index


def get_threshold(dataset):

    x1 = []    #samples
    x2 = []    #hit_rate
    x3 = []    #threshold

    for r in range(0,500,1):
        #print '-----十字星涨幅 ratio-----',r * 0.00001
        index,cross_date = cross_sign(dataset,r * 0.00001)
        # print '总样本数:',len(dataset)
        # print '十字星个数:',len(index)
        if len(index) !=0:
            index3,index4 = get_kline_ud(dataset,index)  #开盘、收盘上升/下降位置
            index5 = get_kline_rise(dataset,index)     #涨幅显著位置
            index_set = set(index).difference(set(index3).union(set(index4)).union(set(index5)))
            #
            # print '满足条件一、二的样本数:',len(index)-len(index_set)
            # print '满足条件一、二的概率:',round(1-len(index_set)/len(index),4)
            # print '\n'
            x1.append(len(index))
            x2.append(round(1-len(index_set)/len(index),4))
            x3.append(r * 0.00001)

    if len(x2) % 2 ==0:#当len(x2)为偶数时,避免中位数取均值,主动删除一行
        a = pd.DataFrame({'samples':x1[1:], 'hit_rate':x2[1:],'threshold':x3[1:]})
    else:
        a = pd.DataFrame({'samples':x1, 'hit_rate':x2,'threshold':x3})
    hit_rate = np.median(x2[:-1])
    b = a[['samples','hit_rate','threshold']][a.hit_rate == hit_rate].sort_values(by='samples')
    threshold_data = pd.DataFrame()
    now = datetime.datetime.now()
    insert_date = now.strftime("%Y-%m-%d %H:%M:%S")

    threshold_data['date'] =  dataset.iloc[-1:]['date_time'].tolist()
    threshold_data['varieties'] = dataset.iloc[-1:]['varieties'].tolist()
    threshold_data['contract'] = dataset.iloc[-1:]['contract'].tolist()
    threshold_data['threshold'] = b.iloc[-1]['threshold']
    threshold_data['insert_date'] = insert_date

    return  threshold_data

def cross_star():
    now = datetime.datetime.now()
    end_date = now.strftime("%Y-%m-%d")
    start_date = '2015-1-1'
    # end_date = '2017-6-28'
    varieties_list = ['cu','zn','al','pb','ni']
    symbol = {'cu':'DST00001','al':'DST00002','zn':'DST00003','pb':'DST00004','ni':'DST00005'}
    for varieties in varieties_list:
        dataset = read_day_kline(varieties,start_date,end_date).dropna(how = 'any')     #读取day_kline
        dataset = pd.concat([dataset],ignore_index=True) #index 重新编号

        threshold_data = get_threshold(dataset)     #十字星阀值
        threshold_data['symbol'] = symbol[varieties]
        to_cross_star_threshold(threshold_data)

        last_date = read_last_history(varieties)    #读取十字星历史表的最新记录时间
        if last_date==None: last_date = '2014-12-30'
        dataset_slice= dataset[dataset['date_time']>last_date]
        history_data = cross_star_history(dataset_slice)   #十字星历史
        to_cross_star_history(history_data)    #十字星历史写入数据库




























