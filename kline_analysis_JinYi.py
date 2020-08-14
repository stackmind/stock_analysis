#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: kline_analysis.py
@time: 2020/08/13
"""
from WindPy import *
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from stock_analysis import get_process_datas
from pyecharts.charts import Line,Grid,Scatter,Kline
from pyecharts import options as opts
import webbrowser as wb

def get_line_peaks(df):
    line = df.values.tolist()
    line_peaks = []
    indexes_peaks, _ = signal.find_peaks(line, distance=1)  # 获得极大值的index
    for i in indexes_peaks:
        line_peaks.append(line[i])
    # print(len(line_peaks))  # 查看极大值极小值序列长度，是不是成对出现
    return indexes_peaks.tolist(),line_peaks

def get_line_valleys(df):
    line = df.values.tolist()
    line_negative = [-x for x in line]  # 取反，则极小值为极大值
    line_valleys = []
    indexes_valleys, _ = signal.find_peaks(line_negative, distance=1)  # 获得极小值的index
    for i in indexes_valleys:
        line_valleys.append(line[i])
    # print(len(line_valleys))  # 查看极大值极小值序列长度，是不是成对出现
    return indexes_valleys.tolist(),line_valleys

def get_daykline_situation(ts_code, start_date, end_date):#获得每日60分钟线数据
    if (os.path.exists('stock_{}/stock_dailychange_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_daily_data = pd.read_csv('stock_{}/stock_dailychange_{}.csv'.format(ts_code,ts_code))
        print('本次日内数据使用本地数据。')
    else:
        w.start()
        error, daily_data = w.wsi(ts_code, "chg", start_date+' 09:00:00', end_date+' 15:31:00', "BarSize=60;PriceAdj=F",
                                 usedf=True)
        w.close()
        if error != 0:
            raise AssertionError("日内数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error, daily_data.values[0][0]))
        daily_data.fillna(0, inplace=True)
        if os.path.exists('stock_{}'.format(ts_code)):
            daily_data.to_csv('stock_{}/stock_dailychange_{}.csv'.format(ts_code,ts_code), index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            daily_data.to_csv('stock_{}/stock_dailychange_{}.csv'.format(ts_code,ts_code), index_label='TIME')
        stock_daily_data = pd.read_csv('stock_{}/stock_dailychange_{}.csv'.format(ts_code,ts_code))
        print('本次日内数据从Windpy网络获取。')
    return stock_daily_data

def find_daily_situation(ts_code, start_date, end_date):#将统计每日小时线中出现的K线排列情况分布


    daily_data = get_daykline_situation(ts_code, start_date, end_date)
    # print(daily_data[:10])

    daily_data['TIME'] = pd.to_datetime(daily_data['TIME'])
    index_temp = daily_data['TIME'].dt.date.drop_duplicates()#舍去时分秒，去除重复项
    indexes = index_temp.apply(lambda x: x.strftime('%Y-%m-%d')).tolist()
    print('总共获得的60分钟线天数:',len(indexes))
    daily_data = daily_data.set_index('TIME')

    #定义16种情况数据分布,从0000到1111，0表示阴线，1表示阳线
    data=[[] for _ in range(16)]
    # print(indexes)
    for i in indexes:
        daily = daily_data[i]['change'].values.tolist()
        # print(daily)
        if (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[0].append(i)#0000
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[1].append(i)#0001
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[2].append(i)#0010
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[3].append(i)#0011
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <=0):
            data[4].append(i)#0100
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[5].append(i)#0101
        elif (daily[0] <= 0 and daily[1] >=0 and daily[2] >= 0 and daily[3] <= 0):
            data[6].append(i)#0110
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[7].append(i)#0111
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[8].append(i)#1000
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[9].append(i)#1001
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[10].append(i)#1010
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[11].append(i)#1011
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[12].append(i)#1100
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[13].append(i)#1101
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >=0 and daily[3] < 0):
            data[14].append(i)#1110
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[15].append(i)#1111
        else:
            print('异常!!!!')

    # print(len(data), data)
    kind = {0: '----', 1: '---+', 2: '--+-', 3: '--++',
           4: '-+--', 5: '-+-+', 6: '-++-', 7: '-+++',
           8: '+---', 9: '+--+', 10: '+-+-', 11: '+-++',
           12: '++--', 13: '++-+', 14: '+++-', 15: '++++'}
    for i in range(16):
        print('所有时间点日内小时K线 {} 分布个数：'.format(kind[i]),len(data[i]),'占比','{:.2f}%'.format(len(data[i])/len(indexes)*100))

    return data

def find_peaks_situation(stock_data,name):#将统计峰谷点每日小时线中出现的K线排列情况分布

    indexes_peaks, values_peaks = get_line_peaks(stock_data[name])  # 获得所有的峰值点
    indexes_valleys, values_valleys = get_line_valleys(stock_data[name])  # 获得所有的谷值点
    line = stock_data[name].values.tolist()  # 寻找极大值极小值的曲线

    # print('数据调整前的峰谷值：')
    # print(len(indexes_peaks), indexes_peaks)
    # print(len(indexes_valleys), indexes_valleys)
    # 极大值和极小值交替出现，确保峰值在前，谷值在后，序列以峰值开头，以谷值结束
    if (indexes_valleys[0] < indexes_peaks[0]):
        indexes_valleys.pop(0)
    if (indexes_valleys[-1] < indexes_peaks[-1]):
        indexes_peaks.pop()
    # print('数据调整后的峰谷值，确保峰值在前，以谷值结束：')
    # print(len(indexes_peaks), indexes_peaks)
    # print(len(indexes_valleys), indexes_valleys)
    print('总共获得的峰值天数：',len(indexes_peaks))
    peaks_date=stock_data.loc[indexes_peaks]["TIME"].tolist()
    stock_data = stock_data.set_index('TIME')
    data = [[] for _ in range(16)]

    daily_data = get_daykline_situation(ts_code, start_date, end_date)
    daily_data['TIME'] = pd.to_datetime(daily_data['TIME'])
    daily_data = daily_data.set_index('TIME')
    # print(peaks_date)
    for i in peaks_date:
        daily = daily_data[i]['change'].values.tolist()
        # print(daily)
        if (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[0].append(i)  # 0000
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[1].append(i)  # 0001
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[2].append(i)  # 0010
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[3].append(i)  # 0011
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[4].append(i)  # 0100
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[5].append(i)  # 0101
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[6].append(i)  # 0110
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[7].append(i)  # 0111
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[8].append(i)  # 1000
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[9].append(i)  # 1001
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[10].append(i)  # 1010
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[11].append(i)  # 1011
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[12].append(i)  # 1100
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[13].append(i)  # 1101
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] < 0):
            data[14].append(i)  # 1110
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[15].append(i)  # 1111
        else:
            print('异常!!!!')

    # print(len(data), data)
    kind={0:'----',1:'---+',2:'--+-',3:'--++',
         4:'-+--',5:'-+-+',6:'-++-',7:'-+++',
         8:'+---',9:'+--+',10:'+-+-',11:'+-++',
         12:'++--',13:'++-+',14:'+++-',15:'++++'}
    for i in range(16):
        print('峰值点日内小时K线 {} 分布个数：'.format(kind[i]), len(data[i]), '占比', '{:.2f}%'.format(len(data[i]) / len(peaks_date) * 100))
    return  data

def find_valleys_situation(stock_data,name):#将统计谷点每日小时线中出现的K线排列情况分布

    indexes_peaks, values_peaks = get_line_peaks(stock_data[name])  # 获得所有的峰值点
    indexes_valleys, values_valleys = get_line_valleys(stock_data[name])  # 获得所有的谷值点
    line = stock_data[name].values.tolist()  # 寻找极大值极小值的曲线

    # print('数据调整前的峰谷值：')
    # print(len(indexes_peaks), indexes_peaks)
    # print(len(indexes_valleys), indexes_valleys)
    # 极大值和极小值交替出现，确保峰值在前，谷值在后，序列以峰值开头，以谷值结束
    if (indexes_valleys[0] < indexes_peaks[0]):
        indexes_valleys.pop(0)
    if (indexes_valleys[-1] < indexes_peaks[-1]):
        indexes_peaks.pop()
    # print('数据调整后的峰谷值，确保峰值在前，以谷值结束：')
    # print(len(indexes_peaks), indexes_peaks)
    # print(len(indexes_valleys), indexes_valleys)
    print('总共获得的谷值天数：',len(indexes_valleys))
    valleys_date=stock_data.loc[indexes_valleys]["TIME"].tolist()
    stock_data = stock_data.set_index('TIME')
    data = [[] for _ in range(16)]

    daily_data = get_daykline_situation(ts_code, start_date, end_date)
    daily_data['TIME'] = pd.to_datetime(daily_data['TIME'])
    daily_data = daily_data.set_index('TIME')
    # print(peaks_date)
    for i in valleys_date:
        daily = daily_data[i]['change'].values.tolist()
        # print(daily)
        if (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[0].append(i)  # 0000
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[1].append(i)  # 0001
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[2].append(i)  # 0010
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[3].append(i)  # 0011
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[4].append(i)  # 0100
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[5].append(i)  # 0101
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[6].append(i)  # 0110
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[7].append(i)  # 0111
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[8].append(i)  # 1000
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[9].append(i)  # 1001
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[10].append(i)  # 1010
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[11].append(i)  # 1011
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[12].append(i)  # 1100
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[13].append(i)  # 1101
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] < 0):
            data[14].append(i)  # 1110
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[15].append(i)  # 1111
        else:
            print('异常!!!!')

    # print(len(data), data)
    kind={0:'----',1:'---+',2:'--+-',3:'--++',
         4:'-+--',5:'-+-+',6:'-++-',7:'-+++',
         8:'+---',9:'+--+',10:'+-+-',11:'+-++',
         12:'++--',13:'++-+',14:'+++-',15:'++++'}
    for i in range(16):
        print('谷值点日内小时K线 {} 分布个数：'.format(kind[i]), len(data[i]), '占比', '{:.2f}%'.format(len(data[i]) / len(valleys_date) * 100))
    return  data

def get_index_by_callback_proportion(stock_data,name):
    indexes_peaks, values_peaks = get_line_peaks(stock_data[name])  # 获得所有的峰值点
    indexes_valleys, values_valleys = get_line_valleys(stock_data[name])  # 获得所有的谷值点
    line = stock_data[name].values.tolist()  # 寻找极大值极小值的曲线

    print('数据调整前的峰谷值：')
    print(len(indexes_peaks), indexes_peaks)
    print(len(indexes_valleys), indexes_valleys)
    # 极大值和极小值交替出现，确保峰值在前，谷值在后，序列以峰值开头，以谷值结束
    if (indexes_valleys[0] < indexes_peaks[0]):
        indexes_valleys.pop(0)
    if (indexes_valleys[-1] < indexes_peaks[-1]):
        indexes_peaks.pop()
    print('数据调整后的峰谷值，确保峰值在前，以谷值结束：')
    print(len(indexes_peaks), indexes_peaks)
    print(len(indexes_valleys), indexes_valleys)

    indexes_callback5=[]
    indexes_callback10 = []
    indexes_callback20 = []
    others=[]
    for i in range(len(indexes_peaks)):

        if (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.05:
            indexes_callback5.append(indexes_peaks[i])

        elif  (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.1:
            indexes_callback10.append(indexes_peaks[i])

        elif (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.2:
            indexes_callback20.append(indexes_peaks[i])

        else :
            others.append(indexes_peaks[i])


    print('回调小于5%的点:')
    print(len(indexes_callback5),indexes_callback5)
    print('回调大于5% 小于10%的点:')
    print(len(indexes_callback10),indexes_callback10)
    print('回调大于10% 小于20%的点:')
    print(len(indexes_callback20),indexes_callback20)
    print('回调大于20%的点:')
    print(len(others), others)
    print(stock_data.loc[indexes_callback20])
    return indexes_callback20,indexes_callback10,indexes_callback5,others

def find_somedays_situation(stock_data,name,indexes):

    print('总共计数的天数：', len(indexes))
    days_date = stock_data.loc[indexes]["TIME"].tolist()
    stock_data = stock_data.set_index('TIME')
    data = [[] for _ in range(16)]

    daily_data = get_daykline_situation(ts_code, start_date, end_date)
    daily_data['TIME'] = pd.to_datetime(daily_data['TIME'])
    daily_data = daily_data.set_index('TIME')

    for i in days_date:
        daily = daily_data[i]['change'].values.tolist()
        # print(daily)
        if (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[0].append(i)  # 0000
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[1].append(i)  # 0001
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[2].append(i)  # 0010
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[3].append(i)  # 0011
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[4].append(i)  # 0100
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[5].append(i)  # 0101
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[6].append(i)  # 0110
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[7].append(i)  # 0111
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[8].append(i)  # 1000
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[9].append(i)  # 1001
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[10].append(i)  # 1010
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[11].append(i)  # 1011
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[12].append(i)  # 1100
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[13].append(i)  # 1101
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] < 0):
            data[14].append(i)  # 1110
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[15].append(i)  # 1111
        else:
            print('异常!!!!')

    # print(len(data), data)
    kind = {0: '----', 1: '---+', 2: '--+-', 3: '--++',
            4: '-+--', 5: '-+-+', 6: '-++-', 7: '-+++',
            8: '+---', 9: '+--+', 10: '+-+-', 11: '+-++',
            12: '++--', 13: '++-+', 14: '+++-', 15: '++++'}
    for i in range(16):
        print('选取的系列点日内小时K线 {} 分布个数：'.format(kind[i]), len(data[i]), '占比',
              '{:.2f}%'.format(len(data[i]) / len(indexes) * 100))
    return data

def draw_charts(stock_data,name):

    x = stock_data['TIME'].values.tolist()
    y = stock_data[name].values.tolist()
    indexes_peaks, line_peaks=get_line_peaks(stock_data[name])
    indexes_valleys, line_valleys=get_line_valleys(stock_data[name])

    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis('收盘价', y, label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False, )
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")],
                             title_opts=opts.TitleOpts(title="股票价格",
                                                       subtitle=ts_code,
                                                       pos_left='15%',
                                                       pos_top="40%"),
                             # 把所有的x轴连接在一起
                             axispointer_opts=opts.AxisPointerOpts(is_show=True,
                                                                   link=[{"xAxisIndex": "all"}],
                                                                   label=opts.LabelOpts(background_color="#777"),
                                                                   ),

                             )

    )

    # 极大值的散点图
    scatter_peak = (
        Scatter()
            .add_xaxis(indexes_peaks)
            .add_yaxis('Peaks', line_peaks, label_opts=opts.LabelOpts(is_show=False), symbol='triangle',
                       symbol_rotate=180, itemstyle_opts=opts.ItemStyleOpts(color='#ef232a'))
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")], )
    )

    scatter_valley = (
        Scatter()
            .add_xaxis(indexes_valleys)
            .add_yaxis('Valleys', line_valleys, label_opts=opts.LabelOpts(is_show=False), symbol='triangle',
                       itemstyle_opts=opts.ItemStyleOpts(color='#14b143'))
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")], )
    )
    #绘制布林带
    line_boll = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="MID",
            y_axis=stock_data["MID"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False,
        )
            .add_yaxis(
            series_name="UPPER",
            y_axis=stock_data["UPPER"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False,
        )
            .add_yaxis(
            series_name="LOWER",
            y_axis=stock_data["LOWER"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False,
        )

            .set_global_opts(datazoom_opts=[opts.DataZoomOpts(type_="inside", )],
                             xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ), )
    )

    stock_basic_data = stock_data[["TIME", "OPEN", "CLOSE", "LOW", "HIGH"]]
    # 绘制K线图
    kline = (
        Kline()
            .add_xaxis(x)
            .add_yaxis("K线图", stock_basic_data.iloc[:, 1:5].values.tolist(), itemstyle_opts=opts.ItemStyleOpts(
            color="#ec0000",
            color0="#00da3c"
        ), )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True,
                                     is_show=False),
            # axis_opts=opts.AxisOpts(is_scale=True,min_=0), #y轴起始坐标可以设为0
            yaxis_opts=opts.AxisOpts(is_scale=True,
                                     splitarea_opts=opts.SplitAreaOpts(is_show=True,
                                                                       areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                                                       ),
                                     ),  # y轴起始坐标可自动调整
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
            legend_opts=opts.LegendOpts(is_show=True, orient='vertical', pos_right="5%", pos_top='20%'),

            datazoom_opts=[  # 设置zoom参数后即可缩放
                opts.DataZoomOpts(
                    is_show=True,
                    type_="inside",

                ),

            ],

        )
    )
    line_close = (
        Line()
            .add_xaxis(x)
            .add_yaxis('五日均线', stock_data["MA5"].values.tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")],
                             )

    )
    overlap_findpeak = line.overlap(scatter_peak)
    overlap_findpeak = overlap_findpeak.overlap(scatter_valley)
    overlap_findpeak = overlap_findpeak.overlap(line_boll)
    overlap_findpeak = overlap_findpeak.overlap(kline)
    overlap_findpeak = overlap_findpeak.overlap(line_close)

    grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))

    grid_chart.add(
        overlap_findpeak,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

    grid_chart.render('stock_{}/find_peak.html'.format(ts_code))


if __name__ == "__main__":
    ts_code = '399441.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2017-08-15'  # 开始日期
    end_date = '2020-08-10'  # 结束日期
    stock_data = get_process_datas(ts_code, start_date, end_date)
    print('总共获得的股票基本数据天数：',len(stock_data))
    print('-' * 50)
    a=find_daily_situation(ts_code, start_date, end_date)
    count1=[]
    label=['----','---+','--+-','--++','-+--','-+-+','-++-','-+++','+---','+--+','+-+-','+-++','++--','++-+','+++-','++++']
    for i in range(len(a)):
        count1.append((label[i],len(a[i])))
    #print(count1)
    print('-'*50)
    b=find_peaks_situation(stock_data,'CLOSE')
    count2 = []
    for i in range(len(b)):
        count2.append((label[i],len(b[i])))
    #print(count2)
    print('-' * 50)
    c=find_valleys_situation(stock_data,'CLOSE')
    count3 = []
    for i in range(len(c)):
        count3.append((label[i], len(c[i])))
    #print(count3)

    indexes_callback20, indexes_callback10, indexes_callback5 ,others= get_index_by_callback_proportion(stock_data, 'CLOSE')
    print('回调5%以内的峰值点小时K线：')
    m=find_somedays_situation(stock_data,'CLOSE',indexes_callback5)
    count4=[]
    print('回调大于5%小于10%的峰值点小时K线：')
    n=find_somedays_situation(stock_data,'CLOSE',indexes_callback10)
    count5=[]
    print('回调大于10%小于20%的峰值点小时K线：')
    j=find_somedays_situation(stock_data, 'CLOSE', indexes_callback20)
    count6=[]
    for i in range(len(m)):
        count4.append((label[i], len(m[i])))
    for i in range(len(n)):
        count5.append((label[i], len(n[i])))
    for i in range(len(j)):
        count6.append((label[i], len(j[i])))
    #draw_charts(stock_data,'CLOSE')
    #wb.open('stock_{}\/find_peak.html'.format(ts_code))

from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

#将列表里的元组按出现天数进行排序，方便后续分析饼图观察前几个天数出现最多的特征
count1 = sorted(count1, key=lambda tup: tup[1])
count2 = sorted(count2, key=lambda tup: tup[1])
count3 = sorted(count3, key=lambda tup: tup[1])
count4 = sorted(count4, key=lambda tup: tup[1])
count5 = sorted(count5, key=lambda tup: tup[1])
count6 = sorted(count6, key=lambda tup: tup[1])
(
    #初始化配置项，内部可设置颜色
    Pie(init_opts=opts.InitOpts(height='1000px',width='2000px'))
    .add(
        #系列名称，即该饼图的名称
        series_name="大盘特征统计汇总",
        #系列数据项，格式为[(key1,value1),(key2,value2)]
        data_pair=count1,
        #通过半径区分数据大小 “radius” 和 “area” 两种
        #rosetype="radius",
        #饼图的半径，设置成默认百分比，相对于容器高宽中较小的一项的一半
        radius="30%",
        #饼图的圆心，第一项是相对于容器的宽度，第二项是相对于容器的高度
        center=["20%", "28%"],
        #标签配置项
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .add(
        series_name="波峰特征统计汇总",
        data_pair=count2,
        #rosetype="radius",
        radius="30%",
        center=["50%", "28%"],
        #标签配置项
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .add(
        series_name="波谷特征统计汇总",
        data_pair=count3,
        #rosetype="radius",
        radius="30%",
        center=["80%", "28%"],
        # 标签配置项
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .add(
        series_name="回调幅度小于5%特征统计汇总",
        data_pair=count4,
        #rosetype="radius",
        radius="30%",
        center=["20%", "72%"],
        # 标签配置项
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .add(
        series_name="回调幅度介于5%与10%特征统计汇总",
        data_pair=count5,
        # rosetype="radius",
        radius="30%",
        center=["50%", "72%"],
        # 标签配置项
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .add(
        series_name="回调幅度介于10%与20%特征统计汇总",
        data_pair=count6,
        # rosetype="radius",
        radius="30%",
        center=["80%", "72%"],
        # 标签配置项
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    #全局设置
    .set_global_opts(
        #设置标题
        title_opts=opts.TitleOpts(
            #名字
            title="生物医药指数统计汇总",
            #组件距离容器左侧的位置
            pos_left="center",
            #组件距离容器上方的像素值
            pos_top="20",
            #设置标题颜色
            title_textstyle_opts=opts.TextStyleOpts(color="#000",font_size=30),
        ),
        #图例配置项，参数 是否显示图里组件
        legend_opts=opts.LegendOpts(is_show=False),
    )
    #系列设置
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        #设置标签颜色
        label_opts=opts.LabelOpts(color="rgba(0, 0, 0, 0.3)",font_size=20,font_style='italic'),
    )
    .render("生物医药指数统计汇总.html")
)
