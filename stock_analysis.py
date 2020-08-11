#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:shihaojie
@file: stock_analysis.py
@time: 2020/07/27
"""
from WindPy import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pyecharts.charts import Page, Kline, Bar, Grid, Line,Scatter
from pyecharts import options as opts
import webbrowser as wb
from pyecharts.commons.utils import JsCode

def get_basic_data(ts_code, start_date, end_date):  # 获取股票基本数据，包括开盘价，最高价，最低价，收盘价，成交量

    if (os.path.exists('stock_{}/stock_basic_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_basic_data = pd.read_csv('stock_{}/stock_basic_{}.csv'.format(ts_code,ts_code))
        print('本次股票基本数据使用本地数据。')
    else:
        w.start()
        error, basic_data = w.wsd(ts_code, "open,high,low,close,volume", start_date, end_date,"PriceAdj=F", usedf=True)
        w.close()
        if error != 0:
            raise AssertionError("API数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error, basic_data.values[0][0]))
        basic_data.fillna(0, inplace=True)
        if os.path.exists('stock_{}'.format(ts_code)):
            basic_data.to_csv('stock_{}/stock_basic_{}.csv'.format(ts_code,ts_code), index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            basic_data.to_csv('stock_{}/stock_basic_{}.csv'.format(ts_code,ts_code), index_label='TIME')

        basic_data.to_csv('stock_{}/stock_basic_{}.csv'.format(ts_code,ts_code), index_label='TIME')
        stock_basic_data = pd.read_csv('stock_{}/stock_basic_{}.csv'.format(ts_code,ts_code))
       # print(stock_basic_data.head())#查看前几行数据
        print('本次股票基本数据从Windpy网络获取。')

    return stock_basic_data


def get_kdj_data(ts_code, start_date, end_date):  # 获取KDJ数据，分三列，分别是K线，D线，J线

    if (os.path.exists('stock_{}/stock_kdj_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_kdj_data = pd.read_csv('stock_{}/stock_kdj_{}.csv'.format(ts_code,ts_code))
        print('本次KDJ使用本地数据。')
    else:
        w.start()
        error1, k_data = w.wsd(ts_code, "KDJ", start_date, end_date, "KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=1;PriceAdj=F", usedf=True)
        error2, d_data = w.wsd(ts_code, "KDJ", start_date, end_date, "KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=2;PriceAdj=F", usedf=True)
        error3, j_data = w.wsd(ts_code, "KDJ", start_date, end_date, "KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=3;PriceAdj=F", usedf=True)
        w.close()
        if error1 != 0:
            raise AssertionError("K数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error1, k_data.values[0][0]))
        if error2 != 0:
            raise AssertionError("D数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error2, d_data.values[0][0]))
        if error3 != 0:
            raise AssertionError("J数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error3, j_data.values[0][0]))
        k_data.rename(columns={'KDJ': 'K'}, inplace=True)
        d_data.rename(columns={'KDJ': 'D'}, inplace=True)
        j_data.rename(columns={'KDJ': 'J'}, inplace=True)

        kdj_data = k_data.join(d_data).join(j_data)
        # print(kdj_data.head())
        kdj_data.fillna(0, inplace=True)
        if os.path.exists('stock_{}'.format(ts_code)):
            kdj_data.to_csv('stock_{}/stock_kdj_{}.csv'.format(ts_code, ts_code), index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            kdj_data.to_csv('stock_{}/stock_kdj_{}.csv'.format(ts_code, ts_code), index_label='TIME')

        stock_kdj_data = pd.read_csv('stock_{}/stock_kdj_{}.csv'.format(ts_code,ts_code))
        print('本次KGJ数据从Windpy网络获取。')

    return stock_kdj_data


def get_ma_data(ts_code, start_date, end_date):  # 获取移动平均线，分别是5日，10日，20日

    if (os.path.exists('stock_{}/stock_ma_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_ma_data = pd.read_csv('stock_{}/stock_ma_{}.csv'.format(ts_code,ts_code))
        print('本次MA使用本地数据。')
    else:
        w.start()
        error1, ma5_data = w.wsd(ts_code, "MA", start_date, end_date, "MA_N=5;PriceAdj=F", usedf=True)
        error2, ma10_data = w.wsd(ts_code, "MA", start_date, end_date, "MA_N=10;PriceAdj=F", usedf=True)
        error3, ma20_data = w.wsd(ts_code, "MA", start_date, end_date, "MA_N=20;PriceAdj=F", usedf=True)
        w.close()
        if error1 != 0:
            raise AssertionError("ma5数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error1, ma5_data.values[0][0]))
        if error2 != 0:
            raise AssertionError("ma10数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error2, ma10_data.values[0][0]))
        if error3 != 0:
            raise AssertionError("ma20数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error3, ma20_data.values[0][0]))
        ma5_data.rename(columns={'MA': 'MA5'}, inplace=True)
        ma10_data.rename(columns={'MA': 'MA10'}, inplace=True)
        ma20_data.rename(columns={'MA': 'MA20'}, inplace=True)

        ma_data = ma5_data.join(ma10_data).join(ma20_data)
        # print(ma_data.head())
        ma_data.fillna(0, inplace=True)
        if os.path.exists('stock_{}'.format(ts_code)):
            ma_data.to_csv('stock_{}/stock_ma_{}.csv'.format(ts_code, ts_code), index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            ma_data.to_csv('stock_{}/stock_ma_{}.csv'.format(ts_code,ts_code), index_label='TIME')


        stock_ma_data = pd.read_csv('stock_{}/stock_ma_{}.csv'.format(ts_code,ts_code))
        print('本次MA数据从Windpy网络获取。')

    return stock_ma_data


def get_macd_data(ts_code, start_date, end_date):  # 获取MACD数据，分别是DIF,DEA,MACD

    if (os.path.exists('stock_{}/stock_macd_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_macd_data = pd.read_csv('stock_{}/stock_macd_{}.csv'.format(ts_code,ts_code))
        print('本次MACD使用本地数据。')
    else:
        w.start()
        error1, dif_data = w.wsd(ts_code, "MACD", start_date, end_date, "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=1;PriceAdj=F",
                                 usedf=True)
        error2, dea_data = w.wsd(ts_code, "MACD", start_date, end_date, "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=2;PriceAdj=F",
                                 usedf=True)
        error3, macd0_data = w.wsd(ts_code, "MACD", start_date, end_date, "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=3;PriceAdj=F",
                                   usedf=True)
        w.close()
        if error1 != 0:
            raise AssertionError("ma5数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error1, dif_data.values[0][0]))
        if error2 != 0:
            raise AssertionError("ma10数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error2, dea_data.values[0][0]))
        if error3 != 0:
            raise AssertionError("ma20数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error3, macd0_data.values[0][0]))
        dif_data.rename(columns={'MACD': 'DIF'}, inplace=True)
        dea_data.rename(columns={'MACD': 'DEA'}, inplace=True)
        macd0_data.rename(columns={'MACD': 'MACD'}, inplace=True)
        # print(dif_data.head())
        # print(dea_data.head())
        # print(macd0_data.head())
        macd_data = dif_data.join(dea_data).join(macd0_data)
        # print(macd_data.head())
        macd_data.fillna(0, inplace=True)
        if os.path.exists('stock_{}'.format(ts_code)):
            macd_data.to_csv('stock_{}/stock_macd_{}.csv'.format(ts_code,ts_code), index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            macd_data.to_csv('stock_{}/stock_macd_{}.csv'.format(ts_code,ts_code), index_label='TIME')

        stock_macd_data = pd.read_csv('stock_{}/stock_macd_{}.csv'.format(ts_code,ts_code))
        print('本次MACD数据从Windpy网络获取。')

    return stock_macd_data


def get_boll_data(ts_code, start_date, end_date):  # 获取布林线，分别是MID，UPPER,LOWER

    if (os.path.exists('stock_{}/stock_boll_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_boll_data = pd.read_csv('stock_{}/stock_boll_{}.csv'.format(ts_code,ts_code))
        print('本次BOLL使用本地数据。')
    else:
        w.start()
        error1, mid_data = w.wsd(ts_code, "BOLL", start_date, end_date, "BOLL_N=20;BOLL_Width=2;BOLL_IO=1;PriceAdj=F", usedf=True)
        error2, upper_data = w.wsd(ts_code, "BOLL", start_date, end_date, "BOLL_N=20;BOLL_Width=2;BOLL_IO=2;PriceAdj=F",usedf=True)
        error3, lower_data = w.wsd(ts_code, "BOLL", start_date, end_date, "BOLL_N=20;BOLL_Width=2;BOLL_IO=3;PriceAdj=F",usedf=True)
        w.close()
        if error1 != 0:
            raise AssertionError("MID数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error1, mid_data.values[0][0]))
        if error2 != 0:
            raise AssertionError("UPPER数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error2, dea_data.values[0][0]))
        if error3 != 0:
            raise AssertionError("LOWER数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error3, macd0_data.values[0][0]))
        mid_data.rename(columns={'BOLL': 'MID'}, inplace=True)
        upper_data.rename(columns={'BOLL': 'UPPER'}, inplace=True)
        lower_data.rename(columns={'BOLL': 'LOWER'}, inplace=True)  # 名字一样，实际上不需要重命名

        boll_data = mid_data.join(upper_data).join(lower_data)
        # print(boll_data.head())
        boll_data.fillna(0, inplace=True)
        if os.path.exists('stock_{}'.format(ts_code)):
            boll_data.to_csv('stock_{}/stock_boll_{}.csv'.format(ts_code,ts_code), index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            boll_data.to_csv('stock_{}/stock_boll_{}.csv'.format(ts_code,ts_code), index_label='TIME')

        stock_boll_data = pd.read_csv('stock_{}/stock_boll_{}.csv'.format(ts_code,ts_code))
        print('本次BOLL数据从Windpy网络获取。')
    return stock_boll_data

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

def find_daily_situation(ts_code, start_date, end_date):#将日线中出现三阴一阳和三阴一阴情况的日子标为1，其他标为0，存入csv的stock analysis文件中。
    daily_data = get_daykline_situation(ts_code, start_date, end_date)
    stock_data = get_process_datas(ts_code, start_date, end_date)
    daily_data['TIME'] = pd.to_datetime(daily_data['TIME'])
    index_temp = daily_data['TIME'].dt.date.drop_duplicates()#舍去时分秒，去除重复项
    indexes = index_temp.apply(lambda x: x.strftime('%Y-%m-%d')).tolist()
    daily_data = daily_data.set_index('TIME')

    data = []
    for i in indexes:
        daily = daily_data[i]['change'].values.tolist()
        if (daily[0] > 0 and daily[1] > 0 and daily[2] > 0 and daily[3] < 0) or (
                daily[0] < 0 and daily[1] < 0 and daily[2] < 0 and daily[3] > 0):
            data.append(i)#寻找三阴一阳和三阳一阴

    stock_data = stock_data.set_index('TIME')
    stock_data['is31situation']=0
    # print(stock_data[:10])
    # print(stock_data.loc[data])
    stock_data.loc[data,'is31situation']=1

    stock_data.to_csv('stock_{}/stock_analysis_{}.csv'.format(ts_code,ts_code), index_label='TIME')

    return data


def find_market_situation():
    pass

def get_process_datas(ts_code, start_date, end_date):#合并获得的数据
    if (os.path.exists('stock_{}/stock_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_data = pd.read_csv('stock_{}/stock_{}.csv'.format(ts_code,ts_code),index_col=0)
        print('本次使用本地数据。')
    else:
        stock_basic_data = get_basic_data(ts_code, start_date, end_date)
        stock_kdj_data = get_kdj_data(ts_code, start_date, end_date)
        stock_ma_data = get_ma_data(ts_code, start_date, end_date)
        stock_macd_data = get_macd_data(ts_code, start_date, end_date)
        stock_boll_data = get_boll_data(ts_code, start_date, end_date)
        stock_data = pd.merge(stock_basic_data,stock_ma_data)
        stock_data = pd.merge(stock_data,stock_kdj_data)
        stock_data = pd.merge(stock_data,stock_macd_data)
        stock_data = pd.merge(stock_data,stock_boll_data)
        stock_data.to_csv('stock_{}/stock_{}.csv'.format(ts_code,ts_code))
        print('本次数据从Windpy网络获取。')
    return stock_data

def draw_chart(stock_data):
    '''
        pyecharts V1 版本开始支持链式调用
       文档地址 https://pyecharts.org/#/zh-cn/
    '''
    stock_data.index = pd.to_datetime(stock_data['TIME'], format="%Y/%m/%d")
    x = stock_data["TIME"].values.tolist()
    stock_basic_data = stock_data[["TIME", "OPEN", "CLOSE", "LOW", "HIGH", "VOLUME"]]
    # stock_data = stock_data.sort_index(ascending=True)  # 倒序，看时间顺序是否正常决定是不是要用
    # k线图
    kline = (
        Kline()
            .add_xaxis(x)
            .add_yaxis("K线图", stock_basic_data.iloc[:, 1:5].values.tolist(), itemstyle_opts=opts.ItemStyleOpts(
            color="#ec0000",
            color0="#00da3c"
        ),)
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
            title_opts=opts.TitleOpts(title="股票价格",
                                      subtitle=ts_code,
                                      pos_left='22%',
                                      pos_top="20%"),
            #把所有的x轴连接在一起
            # axispointer_opts=opts.AxisPointerOpts(is_show=True,
            #                                       link=[{"xAxisIndex": "all"}],
            #                                       label=opts.LabelOpts(background_color="#777"),
            #                                       ),

            datazoom_opts=[  # 设置zoom参数后即可缩放
                opts.DataZoomOpts(
                    is_show=True,
                    type_="inside",
                    xaxis_index=[0,1,2,3,4],  # 设置第0轴和第1轴同时缩放
                    range_start=0,
                    range_end=100,
                ),

            ],

        )
    )
    # 成交量柱形图
    bar_volumn = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("成交量",
                       stock_basic_data["VOLUME"].values.tolist(),
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
            .set_global_opts(title_opts=opts.TitleOpts(title="成交量", pos_left='22%',pos_top="48%"),
                             legend_opts=opts.LegendOpts(is_show=True,orient='vertical',pos_right="5%",pos_top='48%'),
                             )
    )
    #绘制均线图
    line_ma = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="MA5",
            y_axis=stock_data["MA5"].values.tolist(),

            is_hover_animation=False,
            # linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="MA10",
            y_axis=stock_data["MA10"].values.tolist(),

            is_hover_animation=False,

            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="MA20",
            y_axis=stock_data["MA20"].values.tolist(),

            is_hover_animation=False,

            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )

            .set_global_opts(title_opts=opts.TitleOpts(title="MA", pos_left='22%', pos_top="88%"),
                             xaxis_opts=opts.AxisOpts(type_="category",axislabel_opts=opts.LabelOpts(is_show=False),is_scale=True),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")],
                             legend_opts=opts.LegendOpts(is_show=True,orient='vertical',pos_right="5%",pos_top='85%'),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),)
    )
#绘制jdk线
    line_kdj = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="K",
            y_axis=stock_data["K"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="D",
            y_axis=stock_data["D"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="J",
            y_axis=stock_data["J"].values.tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )

            .set_global_opts(title_opts=opts.TitleOpts(title="KDJ", pos_left='22%',pos_top="62%"),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside",)],
                             legend_opts=opts.LegendOpts(is_show=True,orient='vertical',pos_right="7%",pos_top='60%'),
                             xaxis_opts=opts.AxisOpts(is_scale=True,axislabel_opts=opts.LabelOpts(is_show=False),),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),

                             )
    )
    #绘制macd柱状图
    bar_macd=(
        Bar().add_xaxis(x)
        .add_yaxis(series_name='MACD',
                   yaxis_data=stock_data['MACD'].values.tolist(),
                   xaxis_index=2,
                   yaxis_index=2,
                   label_opts=opts.LabelOpts(is_show=False),
                   itemstyle_opts=opts.ItemStyleOpts(
                       color=JsCode(
                           """
                               function(params) {
                                   var colorList;
                                   if (params.data >= 0) {
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
                   .set_global_opts(
                    title_opts=opts.TitleOpts(title="MACD", pos_left='22%', pos_top="75%"),
                    xaxis_opts=opts.AxisOpts(
                    type_="category",
                    grid_index=2,
                    axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=2,
                split_number=4,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=True),
            ),
            legend_opts=opts.LegendOpts(is_show=True,orient='vertical',pos_right="5%",pos_top='70%'),
        )
    )
    #绘制DIF和DEA
    line_macd = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="DIF",
            y_axis=stock_data['DIF'].values.tolist(),
            xaxis_index=2,
            yaxis_index=2,
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="DEA",
            y_axis=stock_data['DEA'].values.tolist(),
            xaxis_index=2,
            yaxis_index=2,
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False,
        )
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    )
    #绘制布林线
    line_boll = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="MID",
            y_axis=stock_data["MID"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="UPPER",
            y_axis=stock_data["UPPER"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="LOWER",
            y_axis=stock_data["LOWER"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )

            .set_global_opts(
                             datazoom_opts=[opts.DataZoomOpts(type_="inside", )],

                             xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),)
    )



    overlap_kline_linema= kline.overlap(line_boll)
    overlap_macd=bar_macd.overlap(line_macd)
    # 使用网格将多张图标组合到一起显示
    grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))

    # 为了把 data.datas 的数据写入到html中作为全局变量,目前无法跨 series 传值
    # demo 中的代码也是用全局变量传的
    grid_chart.add_js_funcs("var barData = {}".format(stock_basic_data.iloc[:, 1:5].values.tolist()))
    grid_chart.add(
        overlap_kline_linema ,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="3%",height="40%"),

    )

    grid_chart.add(
        bar_volumn,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="45%", height="10%"),
    )

    grid_chart.add(
        line_kdj,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="60%", height="10%")
    )
    grid_chart.add(
        overlap_macd,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="72%", height="10%")
    )

    grid_chart.add(
        line_ma,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="85%", height="10%")
    )

    grid_chart.render('stock_{}/stock_{}.html'.format(ts_code,ts_code))  # 保存成用股票代码命名的文档
    return 0

if __name__ == "__main__":
    ts_code = '300347.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2017-08-10'  # 开始日期
    end_date = '2020-08-01'  # 结束日期
    stock_data=get_process_datas(ts_code, start_date, end_date)

    # print(stock_data.head())
    draw_chart(stock_data)
    wb.open('stock_{}\/stock_{}.html'.format(ts_code,ts_code))
    find_daily_situation(ts_code, start_date, end_date)



