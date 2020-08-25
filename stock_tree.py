#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: stock_tree.py
@time: 2020/08/24
"""
from WindPy import *
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.signal as signal
from stock_analysis import get_process_datas,find_daily_situation,get_basic_data
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
    # print(stock_atr_data)
    # stock_atr_data['overbuy'] = 0
    # stock_atr_data.loc[stock_atr_data['MTR'] >= 2*stock_atr_data['ATR'],'overbuy'] = 1
    # print(stock_atr_data['overbuy'].value_counts())
    stock_atr_data['atr_compare']=stock_atr_data['MTR']/stock_atr_data['ATR']
    # print(stock_atr_data)
    stock_atr_data.to_csv('situation.csv')
    return stock_atr_data

def get_some_factors(ts_code, start_date, end_date):
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

def find_daily_situation(ts_code, start_date, end_date):#将统计每日小时线中出现的K线排列情况分布

    daily_data = get_daykline_situation(ts_code, start_date, end_date)
    # print(daily_data[:10])
    daily_data['TIME'] = pd.to_datetime(daily_data['TIME'])
    index_temp = daily_data['TIME'].dt.date.drop_duplicates()#舍去时分秒，去除重复项
    indexes = index_temp.apply(lambda x: x.strftime('%Y-%m-%d')).tolist()
    print('总共获得的60分钟线天数:',len(indexes))
    daily_data = daily_data.set_index('TIME')

    #定义16种情况数据分布,从0000到1111，0表示阴线，1表示阳线
    data=[[] for _ in range(16)]
    # print(indexes)
    for i in indexes:
        daily = daily_data[i]['change'].values.tolist()
        # print(daily)
        if (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[0].append(i)#0000
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[1].append(i)#0001
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[2].append(i)#0010
        elif (daily[0] <= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[3].append(i)#0011
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <=0):
            data[4].append(i)#0100
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[5].append(i)#0101
        elif (daily[0] <= 0 and daily[1] >=0 and daily[2] >= 0 and daily[3] <= 0):
            data[6].append(i)#0110
        elif (daily[0] <= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[7].append(i)#0111
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[8].append(i)#1000
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[9].append(i)#1001
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] <= 0):
            data[10].append(i)#1010
        elif (daily[0] >= 0 and daily[1] <= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[11].append(i)#1011
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] <= 0):
            data[12].append(i)#1100
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] <= 0 and daily[3] >= 0):
            data[13].append(i)#1101
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >=0 and daily[3] <=0):
            data[14].append(i)#1110
        elif (daily[0] >= 0 and daily[1] >= 0 and daily[2] >= 0 and daily[3] >= 0):
            data[15].append(i)#1111
        else:
            print('异常!!!!')

    # print(len(data), data)
    kind = {0: '----', 1: '---+', 2: '--+-', 3: '--++',
           4: '-+--', 5: '-+-+', 6: '-++-', 7: '-+++',
           8: '+---', 9: '+--+', 10: '+-+-', 11: '+-++',
           12: '++--', 13: '++-+', 14: '+++-', 15: '++++'}
    for i in range(16):
        print('所有时间点日内小时K线 {} 分布个数：'.format(kind[i]),len(data[i]),'占比','{:.2f}%'.format(len(data[i])/len(indexes)*100))

    return data
def get_kline_types(ts_code, start_date, end_date):#将k线分布类别one hot表示作为特征
    daily_kline_situation = find_daily_situation(ts_code, start_date, end_date)
    stock_data=get_basic_data(ts_code, start_date, end_date)
    # stock_data['kline_type'] = 0
    stock_data = stock_data.set_index('TIME')
    print(stock_data.head())
    print(daily_kline_situation)
    for i in range(16):
        stock_data.loc[daily_kline_situation[i],'kline_type'] = i

    return stock_data[['kline_type']].reset_index()

def correlation_analysis(data):#对dataframe里的各个参数做相关性分析
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
    plt.savefig('stock_{}/相关性分析.png'.format(ts_code))
    plt.show()

if __name__ == "__main__":
    ts_code = '300347.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2017-09-01'  # 开始日期
    end_date = '2020-08-24'  # 结束日期
    # stock_data = get_process_datas(ts_code, start_date, end_date)
    # print(stock_data)
    stock_atr = find_atr_market_situation(ts_code, start_date, end_date)
    stock_factors = get_some_factors(ts_code, start_date, end_date)
    data = stock_atr.merge(stock_factors)
    data.to_csv('stock_{}/factors.csv'.format(ts_code))
    print(data.head())
    correlation_analysis(data)#相关性分析
    kline_type = get_kline_types(ts_code, start_date, end_date)
    print(kline_type)
    kline_types=pd.get_dummies(kline_type[['kline_type']])
    print(kline_types)







