#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: get_stock_data.py
@time: 2020/08/27
"""
from WindPy import *
import pandas as pd
import os

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
            raise AssertionError("UPPER数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error2, upper_data.values[0][0]))
        if error3 != 0:
            raise AssertionError("LOWER数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error3, lower_data.values[0][0]))
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

def get_some_factors(ts_code, start_date, end_date):#获得一些直接可用的量化因子
    if (os.path.exists('stock_{}/stock_factors_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_factors_data = pd.read_csv('stock_{}/stock_factors_{}.csv'.format(ts_code,ts_code))
        print('本次factors使用本地数据。')
    else:
        w.start()#因子为 对数市值，20日收益方差，一致预测净利润变化率，过去五日价格动量，20日平均换手率，空头力道，市场能量指标
        error, factors_data = w.wsd(ts_code, "val_lnmv,risk_variance20,west_netprofit_fy1_1m,tech_revs5,tech_turnoverrate20,tech_bearpower,tech_cyf", start_date, end_date, "PriceAdj=F", usedf=True)
        w.close()

        if error != 0:
            raise AssertionError("UPPER数据提取错误，ErrorCode={}，错误码含义为'{}'。".format(error, factors_data.values[0][0]))
        # print(boll_data.head())
        factors_data.fillna(0, inplace=True)
        if os.path.exists('stock_{}'.format(ts_code)):
            factors_data.to_csv('stock_{}/stock_factors_{}.csv'.format(ts_code,ts_code), index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            factors_data.to_csv('stock_{}/stock_factors_{}.csv'.format(ts_code,ts_code), index_label='TIME')

        stock_factors_data = pd.read_csv('stock_{}/stock_factors_{}.csv'.format(ts_code,ts_code))
        print('本次factors数据从Windpy网络获取。')
    return stock_factors_data


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
            stock_atr_data.to_csv('stock_{}/stock_atr_{}.csv'.format(ts_code,ts_code),index_label='TIME')
        else:
            os.makedirs('stock_{}'.format(ts_code))
            stock_atr_data.to_csv('stock_{}/stock_atr_{}.csv'.format(ts_code,ts_code), index_label='TIME')

        stock_atr_data = pd.read_csv('stock_{}/stock_atr_{}.csv'.format(ts_code,ts_code))
        print('本次ATR数据从Windpy网络获取。')
    return stock_atr_data

if __name__ == "__main__":
    print()
