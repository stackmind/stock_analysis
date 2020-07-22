# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:14:38 2020

@author: STACK
"""
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
import mplfinance as mpf
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

pro = ts.pro_api()
ts_code='300529.SZ' #此处填写股票号'688399.SH','300347.SZ',
start_data = '20200101' #开始日期
end_data='20200721' #结束日期

daily_data=pro.daily(ts_code = ts_code,start_date = start_data,end_date=end_data)

daily_data.to_csv('stock_{}.csv'.format(ts_code),index_label='index')

stock_data=pd.read_csv('stock_{}.csv'.format(ts_code))

stock_data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'vol': 'Volume'}, inplace=True)
#print(daily_data[:1])
# 转化为日期类型
stock_data.index= pd.to_datetime(stock_data['trade_date'],format="%Y%m%d")
stock_data.index.name='Date'
print(stock_data.head())
#将数据保存到本地csv文件
mpf.plot(stock_data,type='candle',volume=True,show_nontrading=False)#绘制k#mav=(5,10,20),

from pyecharts.charts import Page,Kline,Bar,Grid,Line
from pyecharts import options as opts
import webbrowser as wb

# pyecharts V1 版本开始支持链式调用
#文档地址 https://pyecharts.org/#/zh-cn/
stock_data_extracted=stock_data[["Open","Close","Low","High","Volume"]]
print(stock_data_extracted.head())
#k线
kline=(
    Kline()
    .add_xaxis(stock_data_extracted.index.values.tolist())
    .add_yaxis("K线图", stock_data_extracted.iloc[:,:4].values.tolist())
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True,is_show=False),
        #axis_opts=opts.AxisOpts(is_scale=True,min_=0), #y轴起始坐标可以设为0
        yaxis_opts=opts.AxisOpts(is_scale=True), #y轴起始坐标可自动调整
        title_opts=opts.TitleOpts(title="价格",subtitle=ts_code,pos_top="20%"),
        axispointer_opts=opts.AxisPointerOpts(
            is_show=True,
            link=[{"xAxisIndex": "all"}],
            label=opts.LabelOpts(background_color="#777"),
        ),
        datazoom_opts=[ #设置zoom参数后即可缩放
            opts.DataZoomOpts(
                is_show=True,
                type_="inside",
                xaxis_index=[0,1], #设置第0轴和第1轴同时缩放
                range_start=0,
                range_end=100,
            ),
            opts.DataZoomOpts(
                is_show=True,
                xaxis_index=[0,1],
                type_="slider",
                pos_top="90%",
                range_start=0,
                range_end=100,
            ),
        ],

    )
)


#成交量柱形图
x=stock_data_extracted.index.values.tolist()
y=stock_data_extracted[["Volume"]].values[:,0].tolist()

bar = (
    Bar()
    .add_xaxis(x)
    .add_yaxis("成交量",y,label_opts=opts.LabelOpts(is_show=False),itemstyle_opts=opts.ItemStyleOpts(color="#008080"))
    .set_global_opts(title_opts=opts.TitleOpts(title="成交量",pos_top="70%"),
                     legend_opts=opts.LegendOpts(is_show=False),
                    )
)

#使用网格将多张图标组合到一起显示
grid_chart = Grid()

grid_chart.add(
    kline,
    grid_opts=opts.GridOpts(pos_left="15%", pos_right="8%", height="55%"),
)

grid_chart.add(
    bar,
    grid_opts=opts.GridOpts(pos_left="15%", pos_right="8%", pos_top="70%", height="20%"),
)

grid_chart.render("kline.html")
wb.open("kline.html")
