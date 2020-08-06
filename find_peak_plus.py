#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: find_peak_plus.py
@time: 2020/08/06
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from stock_analysis import get_process_datas
from pyecharts.charts import Line,Grid,Scatter,Kline
from pyecharts import options as opts
import webbrowser as wb
import pandas as pd
def find_peak_plus(df):
    close = df.values.tolist()
    smooth = signal.savgol_filter(close, 11, 5)
    print(len(close) , close)
    print(len(close) , smooth)
    # plt.plot(range(len(close)), close, color='black')
    # plt.plot(range(len(smooth)),smooth, color='green')
    # plt.show()
    indexes=[]
    for i in range(2, len(close) - 2):
        if close[i] > close[i - 1] and close[i] > close[i - 2] and close[i] > close[i + 1] and close[i] > close[i + 2]:
            indexes.append(i)
    print(indexes)
    return indexes




def draw_charts(stock_data):


    x = stock_data['TIME'].values.tolist()
    y1 = stock_data['CLOSE'].values.tolist()
    y2= stock_data['MA5'].values.tolist()
    smooth = signal.savgol_filter(y1, 21, 5)
    indexes = find_peak_plus(stock_data['CLOSE'])
    peaks = []
    for i in indexes:
        peaks.append(y1[i])

    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis('CLOSE', y1, label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False, )
            .add_yaxis('MA5', y2, label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False, )
            .add_yaxis('SMOOTH', smooth, label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False, )
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
            .add_xaxis(indexes)
            .add_yaxis('Peaks', peaks, label_opts=opts.LabelOpts(is_show=False), symbol='triangle',
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
    overlap_findpeak = line.overlap(scatter_peak)

    grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))

    grid_chart.add(
        overlap_findpeak,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

    grid_chart.render('find_peak_plus.html')

if __name__ == "__main__":
    ts_code = '300497.SZ'  # 此处填写股票号'000661.SZ' '300347.SZ' '688399.SH'
    start_date = '2015-12-22'  # 开始日期
    end_date = '2020-08-01'  # 结束日期
    stock_data = get_process_datas(ts_code, start_date, end_date)


    draw_charts(stock_data)
    wb.open('find_peak_plus.html')
