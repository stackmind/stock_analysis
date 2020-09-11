#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: draw_compare.py
@time: 2020/08/21
"""
from WindPy import *
import pandas as pd
import os
import matplotlib.pyplot as plt
from pyecharts.charts import Line,Grid,Scatter
from pyecharts import options as opts
import webbrowser as wb
import seaborn as sns
import matplotlib.pyplot as plt
# #显示所有列
# pd.set_option('display.max_columns', None)
# #显示所有行
# pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)
def get_close_data(ts_codes, start_date, end_date):  # 获取股票基本数据，包括开盘价，最高价，最低价，收盘价，成交量

    if (os.path.exists('stock_close.csv')):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        close_data = pd.read_csv('stock_close.csv')
        print('本次股票收盘数据使用本地')
    else:
        w.start()
        error, close_data = w.wsd(ts_codes, "close", start_date, end_date,"PriceAdj=F", usedf=True)
        w.close()
        if error != 0:
            raise AssertionError("API数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error, close_data.values[0][0]))
        # close_data.fillna(0, inplace=True)

        close_data.to_csv('stock_close.csv', index_label='TIME')

        close_data = pd.read_csv('stock_close.csv')
       # print(stock_basic_data.head())#查看前几行数据
        print('本次股票基本数据从Windpy网络获取。')
    return close_data

def draw_grow_chart(data):
    for i in ts_codes:

        data[i] = data[i].values
        # print(data[i])
        data[i]=data[i]/(data[i][data[i].notnull()].iloc[0])#除以每一列的第一个非空值

    print(data)

    x = data.index.values.tolist()

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

    grid_chart.render('股票增长对比.html')
def draw_dailychange_chart(data):

    x = data.index.values.tolist()

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
                             title_opts=opts.TitleOpts(title="股票涨跌幅对比",

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

    grid_chart.render('股票涨跌幅对比.html')

def draw_situation_chart(data):

    x = data.index.values.tolist()

    scatter = (
        Scatter()
            .add_xaxis(x)
            .add_yaxis('医药生物指数', data['000808.SH'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('天宇股份', data['300702.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('凯普生物', data['300639.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       )
            .add_yaxis('普利制药', data['300630.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('贝达药业', data['300558.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('健帆生物', data['300529.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('富祥药业', data['300497.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('万孚生物', data['300482.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       )
            .add_yaxis('泰格医药', data['300347.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('智飞生物', data['300122.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('安科生物', data['300009.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('凯莱英', data['002821.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       )
            .add_yaxis('长春高新', data['000661.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       )
            .add_yaxis('硕世生物', data['688399.SH'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('健友股份', data['603707.SH'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                       )
            .add_yaxis('安图生物', data['603658.SH'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .add_yaxis('新产业', data['300832.SZ'].tolist(), label_opts=opts.LabelOpts(is_show=False),
                        )
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")],
                             title_opts=opts.TitleOpts(title="股票涨跌情况对比",

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
        scatter,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

    grid_chart.render('股票涨跌情况对比.html')
def correlation_analysis(data,title):#对dataframe里的各个参数做相关性分析
    corr = data.corr(method='pearson')  # 使用皮尔逊系数计算列与列的相关性
    # corr=data.corr(method='kendall')# 肯德尔秩相关系数
    # corr=data.corr(method='spearman')# 斯皮尔曼秩相关系数
    # print(corr)
    fig, ax = plt.subplots(figsize=(10, 10))  # 分辨率1200×1000
    cmap = sns.diverging_palette(220, 10,
                                 as_cmap=True)  # 在两种HUSL颜色之间制作不同的调色板。图的正负色彩范围为220、10，结果为真则返回matplotlib的colormap对象
    fig = sns.heatmap(
        corr,  # 使用Pandas DataFrame数据，索引/列信息用于标记列和行
        cmap=cmap,  # 数据值到颜色空间的映射
        square=True,  # 每个单元格都是正方形
        cbar_kws={'shrink': .9},  # `fig.colorbar`的关键字参数
        ax=ax,  # 绘制图的轴
        annot=True,  # 在单元格中标注数据值
        annot_kws={'fontsize': 8})  # 热图，将矩形数据绘制为颜色编码矩阵

    plt.ylim(0, len(corr))  # 解决y轴文字错乱
    plt.gcf().subplots_adjust(left=0.2, bottom=0.2)  # 解决show图时底部显示不全
    plt.tight_layout()  # 解决坐标文字显示不全###
    plt.savefig(title+'.png')
    plt.show()

if __name__ == "__main__":
    ts_codes = ['000808.SH','300702.SZ','300347.SZ','300639.SZ','300630.SZ','300558.SZ','300529.SZ','300497.SZ','300482.SZ',
                '300122.SZ','300009.SZ','002821.SZ','000661.SZ','688399.SH','603707.SH','603658.SH','300832.SZ']  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2020-01-01'  # 开始日期
    end_date = '2020-08-31'  # 结束日期
    data=get_close_data(ts_codes, start_date, end_date)
    data=data.set_index('TIME')
    print('对股票收盘价统计分析')
    print(data.head())
    print(data.describe())#对股票收盘价进行统计
    data.describe().to_csv('data_describe.csv')

    data_change=data.pct_change()*100#计算每日变化率
    print('对股票每日涨跌统计分析')
    print(data_change.head())
    print(data_change.describe())
    data_change.describe().to_csv('data_change_describe.csv')

    draw_grow_chart(data)
    wb.open('股票增长对比.html')
    draw_dailychange_chart(data_change)
    wb.open('股票涨跌幅对比.html')

    correlation_analysis(data, '股票收盘价相关性分析')
    correlation_analysis(data_change, '股票涨跌幅相关性分析')

    print('股票涨跌幅相关性矩阵')
    print(data_change.cov())
    cov=data_change.cov()
    fig, ax = plt.subplots(figsize=(10, 10))  # 分辨率1200×1000
    cmap = sns.diverging_palette(220, 10,
                                 as_cmap=True)  # 在两种HUSL颜色之间制作不同的调色板。图的正负色彩范围为220、10，结果为真则返回matplotlib的colormap对象
    fig = sns.heatmap(
        cov,  # 使用Pandas DataFrame数据，索引/列信息用于标记列和行
        cmap=cmap,  # 数据值到颜色空间的映射
        square=True,  # 每个单元格都是正方形
        cbar_kws={'shrink': .9},  # `fig.colorbar`的关键字参数
        ax=ax,  # 绘制图的轴
        annot=True,  # 在单元格中标注数据值
        annot_kws={'fontsize': 8})  # 热图，将矩形数据绘制为颜色编码矩阵

    plt.ylim(0, len(cov))  # 解决y轴文字错乱
    plt.gcf().subplots_adjust(left=0.2, bottom=0.2)  # 解决show图时底部显示不全
    plt.tight_layout()  # 解决坐标文字显示不全###
    plt.show()

    draw_situation_chart(data_change)
    wb.open('股票涨跌情况对比.html')

    data_situation = data_change.copy()
    data_situation[data_situation > 0] = 1
    data_situation[data_situation == 0] = 0
    data_situation[data_situation < 0] = -1

    data_situation.describe().to_csv('data_situation_describe.csv')
    print(data_situation.describe())



