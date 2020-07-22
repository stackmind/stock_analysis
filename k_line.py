#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:shihaojie
@file: k_line.py.py
@time: 2020/07/21
"""
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()#使用seaborn，画图美观
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()#控制futurewaring 报错信息
import mplfinance as mpf
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号

def show_close_daily(tscode,start_data,end_data):#绘制
    daily_data=pro.daily(ts_code = tscode,start_date = start_data,end_date=end_data)
    daily_data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'vol': 'Volume'}, inplace=True)
    #print(daily_data[:1])
    # 转化为日期类型
    daily_data.index= pd.to_datetime(daily_data['trade_date'],format="%Y%m%d")
    daily_data.index.name=['Date']
    print(daily_data.head())
    daily_data = daily_data.sort_index(ascending=True)#倒序
    print(daily_data.head())
    # 绘图
    mpf.plot(daily_data,type='candle',mav=(5,10,20),volume=True,show_nontrading=True)#绘制k
#ts.set_token('a52a8119d78a018a4559c35a64866ec6f46feb44ab26f59837a0555d')#注册获取token
pro = ts.pro_api()
ts_codes=['300529.SZ'] #此处填写股票号'688399.SH','300347.SZ',
start_data = '20200101' #开始日期
end_data='20200721' #结束日期
for ts_code in ts_codes:
    show_close_daily(ts_code,start_data,end_data)

