#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: find_daily_situation.py
@time: 2020/08/10
"""
import pandas as pd
from pyecharts.charts import Grid, Line,Scatter
from pyecharts import options as opts
from stock_analysis import get_process_datas,get_daykline_situation
import webbrowser as wb

if __name__ == "__main__":
    ts_code = '300347.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2017-08-10'  # 开始日期
    end_date = '2020-08-01'  # 结束日期
    stock_data = get_process_datas(ts_code, start_date, end_date)

    # print(stock_data.head())
    # draw_chart(stock_data)
    # wb.open('stock_{}.html'.format(ts_code))
    daily_data = get_daykline_situation(ts_code, start_date, end_date)
    print(daily_data)

    print(type(daily_data['TIME']))

    daily_data['TIME'] = pd.to_datetime(daily_data['TIME'])
    index_temp = daily_data['TIME'].dt.date.drop_duplicates()
    indexes = index_temp.apply(lambda x: x.strftime('%Y-%m-%d')).tolist()
    daily_data = daily_data.set_index('TIME')
    # print(indexes)
    data = []
    for i in indexes:
        daily = daily_data[i]['change'].values.tolist()
        # print(i)
        if (daily[0] > 0 and daily[1] > 0 and daily[2] > 0 and daily[3] < 0) or (
                daily[0] < 0 and daily[1] < 0 and daily[2] < 0 and daily[3] > 0):
            data.append(i)

    print(data)
    print(len(data))
    stock_data = stock_data.set_index('TIME')
    stock_data['CLOSE'].plot()
    # stock_data.loc[data]['CLOSE'].plot()
    x1 = stock_data.index.values.tolist()
    y1 = stock_data['CLOSE'].values.tolist()
    # print(stock_data.loc[data]['CLOSE'])
    x2 = stock_data.loc[data].index.tolist()
    y2 = stock_data.loc[data]['CLOSE'].tolist()

    line = (
        Line()
            .add_xaxis(x1)
            .add_yaxis('CLOSE', y1, label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False, )
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
    scatter = (
        Scatter()
            .add_xaxis(x2)
            .add_yaxis('3-1', y2, label_opts=opts.LabelOpts(is_show=False), symbol='triangle',
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
    overlap = line.overlap(scatter)

    grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))

    grid_chart.add(
        overlap,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

    grid_chart.render('stock_dailysituation_{}.html'.format(ts_code))
    wb.open('stock_dailysituation_{}.html'.format(ts_code))
