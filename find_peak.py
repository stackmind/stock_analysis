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
x_=stock_data['TIME'].values
close_= stock_data['CLOSE'].values
choose_data=[]
for i in signal.argrelextrema(close_,np.greater)[0]:
    choose_data.append(x[i])
choose_close = close[signal.argrelextrema(close,np.greater)]
print(choose_data)
print(choose_close)
print(len(choose_data),len(choose_close))
print(type(choose_data),type(choose_close))

# plt.figure(figsize=(12,4))
# plt.plot(np.arange(len(x)),x)
# plt.plot(signal.argrelextrema(x,np.greater)[0],x[signal.argrelextrema(x, np.greater)],'o')
# plt.plot(signal.argrelextrema(-x,np.greater)[0],x[signal.argrelextrema(-x, np.greater)],'+')
#
# plt.show()

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
scatter = (
    Scatter()
        .add_xaxis(choose_data)
        .add_yaxis('Close',choose_close,label_opts=opts.LabelOpts(is_show=False),)
        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        datazoom_opts=[opts.DataZoomOpts(type_="inside")],)

)
overlap_findpeak= line.overlap(scatter)

grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))
grid_chart.add(
        line,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

grid_chart.add(
        scatter,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

# grid_chart.render('find_peak.html')
# wb.open('find_peak.html')
scatter.render('scatter.html')
wb.open('scatter.html')

