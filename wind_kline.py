#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:shihaojie
@file: wind_kline.py
@time: 2020/07/23
"""
from WindPy import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pyecharts.charts import Page, Kline, Bar, Grid, Line
from pyecharts import options as opts
import webbrowser as wb
from pyecharts.commons.utils import JsCode
def calculate_ma(day_count: int, data):
    result: List[Union[float, str]] = []
    for i in range(len(data["values"])):
        if i < day_count:
            result.append("-")
            continue
        sum_total = 0.0
        for j in range(day_count):
            sum_total += float(data["values"][i - j][1])
        result.append(abs(float("%.3f" % (sum_total / day_count))))
    return result

def get_data(tscode,start_date,end_date) -> list:

    if(os.path.exists('stock_{}.csv'.format(ts_code))):#判断本地是否存在文档，若没有则调用接口
    #将数据保存到本地csv文件
        stock_data=pd.read_csv('stock_{}.csv'.format(ts_code))
        print('本次使用本地数据。')
    else:
        w.start()
        error,data=w.wsd(ts_code, "open,high,low,close,volume", start_date, end_date,usedf=True)
        if error != 0:
            raise AssertionError("API数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error,data.values[0][0]))
        #print(data.head() )#查看前几行数据
        data.to_csv('stock_{}.csv'.format(ts_code),index_label='TIME')
        stock_data = pd.read_csv('stock_{}.csv'.format(ts_code))
        print('本次数据从Windpy网络获取。')
    return stock_data

def draw_kine(stock_data):
    '''
        pyecharts V1 版本开始支持链式调用
       文档地址 https://pyecharts.org/#/zh-cn/
    '''
    stock_data.index = pd.to_datetime(stock_data['TIME'], format="%Y/%m/%d")
    stock_data = stock_data[["TIME", "OPEN", "CLOSE", "LOW", "HIGH", "VOLUME"]]
    # stock_data = stock_data.sort_index(ascending=True)  # 倒序，看时间顺序是否正常
    # k线图
    kline = (
        Kline()
            .add_xaxis(stock_data[["TIME"]].values.tolist())
            .add_yaxis("K线图", stock_data.iloc[:, 1:5].values.tolist(),itemstyle_opts=opts.ItemStyleOpts(
            color="#ec0000",
            color0="#00da3c"
            ),
            )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True,
                                     is_show=False),
            # axis_opts=opts.AxisOpts(is_scale=True,min_=0), #y轴起始坐标可以设为0
            yaxis_opts=opts.AxisOpts(is_scale=True,
                                     splitarea_opts=opts.SplitAreaOpts(is_show=True,
                                                                       areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                                                       ),
                                     ),  # y轴起始坐标可自动调整
            title_opts=opts.TitleOpts(title="价格",
                                      subtitle=ts_code,
                                      pos_top="20%"),
            axispointer_opts=opts.AxisPointerOpts(is_show=True,
                                                  link=[{"xAxisIndex": "all"}],
                                                  label=opts.LabelOpts(background_color="#777"),
            ),

            datazoom_opts=[  # 设置zoom参数后即可缩放
                opts.DataZoomOpts(
                    is_show=True,
                    type_="inside",
                    xaxis_index=[0, 1],  # 设置第0轴和第1轴同时缩放
                    range_start=0,
                    range_end=100,
                ),
                opts.DataZoomOpts(
                    is_show=True,
                    xaxis_index=[0, 1],
                    type_="slider",
                    pos_top="90%",
                    range_start=0,
                    range_end=100,
                ),

            ],
            brush_opts=opts.BrushOpts(
                x_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX",
            ),


        )
    )

    # 成交量柱形图
    x = stock_data[["TIME"]].values.tolist()
    y = stock_data[["VOLUME"]].values[:, 0].tolist()

    bar = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("成交量",
                       y,
                       xaxis_index=1,
                       yaxis_index=1,
                       label_opts=opts.LabelOpts(is_show=False),
                       itemstyle_opts=opts.ItemStyleOpts(
                           color=JsCode(
                               """
                           function(params) {
                               var colorList;
                               if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                                   colorList = '#ef232a';
                                   
                               } else {
                                   colorList = '#14b143';
                               }
                               return colorList;
                           }
                           """
                           )
                       ),
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title="成交量", pos_top="70%"),
                             legend_opts=opts.LegendOpts(is_show=False),
                             )
    )

    # 使用网格将多张图标组合到一起显示
    grid_chart = Grid(init_opts=opts.InitOpts(
            width="1200px",
            height="600px",
            animation_opts=opts.AnimationOpts(animation=False),
        ))

    # 这个是为了把 data.datas 这个数据写入到 html 中,还没想到怎么跨 series 传值
    # demo 中的代码也是用全局变量传的
    grid_chart.add_js_funcs("var barData = {}".format(stock_data.iloc[:, 1:5].values.tolist()))
    grid_chart.add(
        kline,
        grid_opts=opts.GridOpts(pos_left="15%", pos_right="15%", height="55%"),
    )

    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(pos_left="15%", pos_right="15%", pos_top="70%", height="20%"),
    )

    grid_chart.render('stock_{}.html'.format(ts_code))#保存成用股票代码命名的文档

if __name__ == "__main__":
    ts_code='300347.SZ' #此处填写股票号'688399.SH','300347.SZ',
    start_date = '2020-01-01' #开始日期
    end_date='2020-07-21' #结束日期
    datepath='stock_date'
    stock_data=get_data(ts_code,start_date, end_date)
    # print(stock_data.head())
    draw_kine(stock_data)
    wb.open('stock_{}.html'.format(ts_code))


