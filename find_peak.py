#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:shihaojie
@file: find_peak.py
@time: 2020/07/30
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from stock_analysis import get_basic_data
from pyecharts.charts import Line,Grid,Scatter
from pyecharts import options as opts
import webbrowser as wb

ts_code = '688399.SH'  # 此处填写股票号'688399.SH'
start_date = '2020-01-01'  # 开始日期
end_date = '2020-07-21'  # 结束日期

stock_data = get_basic_data(ts_code, start_date, end_date)
x = stock_data['TIME'].values.tolist()
close = stock_data['CLOSE'].values.tolist()
close_valley=[-x for x in close]
print(close)
print(close_valley)

close_peaks=[]
close_valleys=[]
indexes, _ = signal.find_peaks(close, distance=1)
print(indexes)
indexes_valley, _ = signal.find_peaks(close_valley, distance=1)
print(indexes_valley)
for i in indexes:
    close_peaks.append(close[i])
for i in indexes_valley:
    close_valleys.append(close[i])
print(close_peaks)
print(close_valleys)
print(len(close_valleys),len(close_peaks))

line = (
    Line()
        .add_xaxis(x)
        .add_yaxis('Close',close,label_opts=opts.LabelOpts(is_show=False),)
        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        datazoom_opts=[opts.DataZoomOpts(type_="inside")],)

)
scatter_top = (
    Scatter()
        .add_xaxis(indexes_valley.tolist())
        .add_yaxis('Close',close_valleys,label_opts=opts.LabelOpts(is_show=False),)
        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        datazoom_opts=[opts.DataZoomOpts(type_="inside")],)
)


overlap_findpeak= line.overlap(scatter_top)

grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))
grid_chart.add(
        overlap_findpeak,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

grid_chart.render('find_peak.html')
wb.open('find_peak.html')


