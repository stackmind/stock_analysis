#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:shihaojie
@file: k_line.py.py
@time: 2020/07/21
"""

# coding: utf-8
import os, sys
import datetime
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
# import matplotlib.finance as mpf
import mplfinance as mpf
import pandas as pd
import tushare as ts

##绘制K线图+移动平均线

if len(sys.argv) == 2:
    code = sys.argv[1]
else:
    print('usage: python mpf_kline.py stockcode ')
    sys.exit(1)

if len(code) != 6:
    print('stock code length: 6')
    sys.exit(2)

# help(ts.get_hist_data) 了解参数
dh = ts.get_hist_data(code)
df = dh.sort_values(by='date')
# print(df.head())
df = df[df.index > '2020-01-01']
if len(df) < 10:
    print(" len(df) <10 ")
    sys.exit(2)

# 对tushare获取到的数据转换成 candlestick_ohlc()方法可读取的格式
alist = []
tlist = []
for date, row in df.iterrows():
    open, high, close, low, volume, price_change, p_change, ma5, ma10, ma20, v_ma5, v_ma10, v_ma20 = row[0:]
    # 将日期转换为数字
    date1 = datetime.datetime.strptime(date, '%Y-%m-%d')
    t = date2num(date1)
    data = (t, open, high, low, close)
    alist.append(data)
    tlist.append(t)

# 加这个两句 可以显示中文
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建子图
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
# 设置X轴刻度为日期时间
ax.xaxis_date()
ax.autoscale_view()
# plt.setp(plt.gca().get_xticklabels(), rotation=45)
plt.xticks(rotation=45)
plt.yticks()
plt.title("股票 {0}：K线图".format(code))
plt.xlabel("date")
plt.ylabel("price")
mpf.candlestick_ohlc(ax, alist, colorup='red', colordown='green')
#  画 10,20日均线
plt.plot(tlist, df['ma10'].values, 'blue', label='ma10')
plt.plot(tlist, df['ma20'].values, 'g--', label='ma20')
plt.legend(loc='best', shadow=True)
plt.grid()
plt.show()

