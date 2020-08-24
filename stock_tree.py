#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: stock_tree.py
@time: 2020/08/24
"""
from WindPy import *
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from stock_analysis import get_process_datas,find_daily_situation
from pyecharts.charts import Line,Grid,Scatter,Kline
from pyecharts import options as opts
import webbrowser as wb
import pandas as pd
def get_atr_data(ts_code, start_date, end_date):
    if (os.path.exists('stock_{}/stock_atr_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_atr_data = pd.read_csv('stock_{}/stock_atr_{}.csv'.format(ts_code,ts_code))
        print('本次ATR使用本地数据。')
    else:
        w.start()
        error1, tr_data = w.wsd(ts_code, "ATR", start_date, end_date, "ATR_N=1;ATR_IO=1;PriceAdj=F", usedf=True)
        error2, atr_data = w.wsd(ts_code, "ATR", start_date, end_date, "ATR_N=14;ATR_IO=2;PriceAdj=F",usedf=True)
        w.close()
        if error1 != 0:
            raise AssertionError("MID数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error1, tr_data.values[0][0]))
        if error2 != 0:
            raise AssertionError("UPPER数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error2, atr_data.values[0][0]))

        tr_data.rename(columns={'ATR': 'MTR'}, inplace=True)
        atr_data.rename(columns={'ATR': 'ATR'}, inplace=True)

        stock_atr_data = tr_data.join(atr_data)
        # print(boll_data.head())
        stock_atr_data.fillna(0, inplace=True)
        if os.path.exists('stock_{}'.format(ts_code)):
            stock_atr_data.to_csv('stock_{}/stock_atr_{}.csv'.format(ts_code,ts_code), index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            stock_atr_data.to_csv('stock_{}/stock_atr_{}.csv'.format(ts_code,ts_code), index_label='TIME')

        stock_atr_data = pd.read_csv('stock_{}/stock_atr_{}.csv'.format(ts_code,ts_code))
        print('本次ATR数据从Windpy网络获取。')
    return stock_atr_data
def find_atr_market_situation(ts_code, start_date, end_date):
    stock_atr_data = get_atr_data(ts_code, start_date, end_date)
    print(stock_atr_data)
    stock_atr_data['overbuy'] = 0
    stock_atr_data.loc[stock_atr_data['ATR'] >= 2*stock_atr_data['MTR'],'overbuy'] = 1
    print(stock_atr_data)
    stock_atr_data.to_csv('situation.csv')
    print(stock_atr_data['overbuy'].value_counts())
    # stock_kdj_data['K1']=0
    # stock_kdj_data.loc[stock_kdj_data['K'] > 80,'K1']= 1
    # stock_kdj_data.loc[stock_kdj_data['K'] < 20, 'K1'] = 2
    # stock_kdj_data['D1'] = 0
    # stock_kdj_data.loc[stock_kdj_data['D'] > 80, 'D1'] = 1
    # stock_kdj_data.loc[stock_kdj_data['D'] < 20, 'D1'] = 2
    # stock_kdj_data['J1'] = 0
    # stock_kdj_data.loc[stock_kdj_data['J'] > 100, 'J1'] = 1
    # stock_kdj_data.loc[stock_kdj_data['J'] < 0, 'J1'] = 2
    # return stock

if __name__ == "__main__":
    ts_code = '300347.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2017-08-10'  # 开始日期
    end_date = '2020-08-01'  # 结束日期
    # stock_data = get_process_datas(ts_code, start_date, end_date)
    # print(stock_data)
    find_atr_market_situation(ts_code, start_date, end_date)

