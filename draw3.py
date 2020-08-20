#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: draw3.py
@time: 2020/08/20
"""
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pyecharts.charts import Line,Grid,Scatter,Kline
from pyecharts import options as opts
import webbrowser as wb

if __name__ == "__main__":
    data=pd.read_csv('16个股票分析.csv',encoding='unicode_escape')
    fig = plt.figure(figsize=(16, 10))
    time=data['DateTime']
    print(data.head())
    data['300702.SZ'] = data['300702.SZ'].values
    data['300702.SZ'] = data['300702.SZ'] / data['300702.SZ'][0]

    data['300639.SZ'] = data['300639.SZ'].values
    data['300639.SZ'] = data['300639.SZ'] / data['300639.SZ'][0]

    data['300630.SZ'] = data['300630.SZ'].values
    data['300630.SZ'] = data['300630.SZ'] / data['300630.SZ'][0]

    data['300558.SZ'] = data['300558.SZ'].values
    data['300558.SZ'] = data['300558.SZ'] / data['300558.SZ'][0]

    data['300529.SZ'] = data['300529.SZ'].values
    data['300529.SZ'] = data['300529.SZ'] / data['300529.SZ'][0]

    data['300497.SZ'] = data['300497.SZ'].values
    data['300497.SZ'] = data['300497.SZ'] / data['300497.SZ'][0]

    data['300482.SZ'] = data['300482.SZ'].values
    data['300482.SZ'] = data['300482.SZ'] / data['300482.SZ'][0]

    data['300347.SZ'] = data['300347.SZ'].values
    data['300347.SZ'] = data['300347.SZ'] / data['300347.SZ'][0]

    data['300122.SZ'] = data['300122.SZ'].values
    data['300122.SZ'] = data['300122.SZ'] / data['300122.SZ'][0]

    data['300009.SZ'] = data['300009.SZ'].values
    data['300009.SZ'] = data['300009.SZ'] / data['300009.SZ'][0]

    data['002821.SZ'] = data['002821.SZ'].values
    data['002821.SZ'] = data['002821.SZ'] / data['002821.SZ'][0]

    data['000661.SZ'] = data['000661.SZ'].values
    data['000661.SZ'] = data['000661.SZ'] / data['000661.SZ'][0]

    data['688399.SH'] = data['688399.SH'].values
    data['688399.SH'] = data['688399.SH'] / data['688399.SH'][0]

    data['603707.SH'] = data['603707.SH'].values
    data['603707.SH'] = data['603707.SH'] / data['603707.SH'][0]

    data['603658.SH'] = data['603658.SH'].values
    data['603658.SH'] = data['603658.SH'] / data['603658.SH'][0]

    data['000808.SH'] = data['000808.SH'].values
    data['000808.SH'] = data['000808.SH'] / data['000808.SH'][0]

    data['300832.SZ'] = data['300832.SZ'].values#新产业上市时间短
    data['300832.SZ'] = data['300832.SZ'] / 45.2

    x = data['DateTime'].values.tolist()

    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis('医药生物指数', data['000808.SH'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('天宇股份', data['300702.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('凯普生物', data['300639.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('普利制药', data['300630.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('贝达药业', data['300558.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('健帆生物', data['300529.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('富祥药业', data['300497.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('万孚生物', data['300482.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('泰格医药', data['300347.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('智飞生物', data['300122.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('安科生物', data['300009.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('凯莱英', data['002821.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('长春高新', data['000661.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('硕世生物', data['688399.SH'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('健友股份', data['603707.SH'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('安图生物', data['603658.SH'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .add_yaxis('新产业', data['300832.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")],
                             title_opts=opts.TitleOpts(title="股票价格增长对比",

                                                       pos_left='10%',
                                                       pos_top="40%"),
                             # 把所有的x轴连接在一起
                             axispointer_opts=opts.AxisPointerOpts(is_show=True,
                                                                   link=[{"xAxisIndex": "all"}],
                                                                   label=opts.LabelOpts(background_color="#777"),
                                                                   ),

                             )

    )
    grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))

    grid_chart.add(
       line,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

    grid_chart.render('16个股票和医药生物指数增长对比.html')
    wb.open('16个股票和医药生物指数增长对比.html')
    print(data['300832.SZ'].tolist())
