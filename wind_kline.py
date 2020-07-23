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

def get_data():

    if(os.path.exists('stock_{}.csv'.format(ts_code))):#判断本地是否存在文档，若没有则调用接口
    #将数据保存到本地csv文件
        stock_data=pd.read_csv('stock_{}.csv'.format(ts_code))
        print('本次使用本地数据。')
    else:
        w.start()
        error,data=w.wsd(ts_code, "open,high,low,close,volume", start_data, end_data,usedf=True)
        if error != 0:
            raise AssertionError("API数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error,data.values[0][0]))
        #print(data.head() )#查看前几行数据
        data.to_csv('stock_{}.csv'.format(ts_code),index_label=None)
        stock_data = pd.read_csv('stock_{}.csv'.format(ts_code))
        print('本次数据从Windpy网络获取。')
    return stock_data

if __name__ == "__main__":
    ts_code='300347.SZ' #此处填写股票号'688399.SH','300347.SZ',
    start_data = '2020-01-01' #开始日期
    end_data='2020-07-21' #结束日期
    datepath='stock_date'
    stock_data=get_data()
    print(stock_data.head())