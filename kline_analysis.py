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
from stock_analysis import get_process_datas,find_daily_situation
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

    return daily

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
    return  daily

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
    return  daily

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
    end_date = '2020-08-01'  # 结束日期
    stock_data = get_process_datas(ts_code, start_date, end_date)
    print('总共获得的股票基本数据天数：',len(stock_data))
    print('-' * 50)
    find_daily_situation(ts_code, start_date, end_date)
    print('-'*50)
    find_peaks_situation(stock_data,'CLOSE')
    print('-' * 50)
    find_valleys_situation(stock_data,'CLOSE')
    draw_charts(stock_data,'CLOSE')
    wb.open('stock_{}\/find_peak.html'.format(ts_code))
