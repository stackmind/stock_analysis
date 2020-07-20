# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:55:05 2020

@author: STACK
"""

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt


ts.set_token('a52a8119d78a018a4559c35a64866ec6f46feb44ab26f59837a0555d')#注册获取token
pro = ts.pro_api()
df1 = pro.daily(ts_code = '600600.SH',start_date = '20170101',end_date='20200717')
df2 = pro.daily(ts_code = '300529.SZ',start_date = '20170101',end_date='20200717')
#转化为日期类型
df1['trade_date'] = pd.to_datetime(df1['trade_date'], format="%Y%m%d")
df2['trade_date'] = pd.to_datetime(df2['trade_date'], format="%Y%m%d")
#绘图
figure = plt.figure(figsize=(18,10))
plt.plot(df1['trade_date'], df1['close'], '-', label = df1.ts_code[0])
plt.plot(df2['trade_date'], df2['close'], '-', label = df2.ts_code[0])
plt.gcf().autofmt_xdate()
#显示文字
plt.legend()
#显示图片
plt.show()
