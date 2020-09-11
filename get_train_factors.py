#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: get_train_factors.py
@time: 2020/08/27
本部分主要负责处理数据，包括因子的处理，获得峰值点，为分类打数据标签等
"""
from get_stock_data import *
import scipy.signal as signal
import numpy as np

def get_line_peaks(df):
    line = df.values.tolist()
    line_peaks = []
    indexes_peaks, _ = signal.find_peaks(line, distance=1)  # 获得极大值的index
    for i in indexes_peaks:
        line_peaks.append(line[i])
    # print(len(line_peaks))  # 查看极大值极小值序列长度，是不是成对出现
    return indexes_peaks.tolist(),line_peaks

def get_line_valleys(df):
    line = df.values.tolist()
    line_negative = [-x for x in line]  # 取反，则极小值为极大值
    line_valleys = []
    indexes_valleys, _ = signal.find_peaks(line_negative, distance=1)  # 获得极小值的index
    for i in indexes_valleys:
        line_valleys.append(line[i])
    # print(len(line_valleys))  # 查看极大值极小值序列长度，是不是成对出现
    return indexes_valleys.tolist(),line_valleys

def find_atr_market_situation(ts_code, start_date, end_date):
    stock_atr_data = get_atr_data(ts_code, start_date, end_date)
    stock_atr_data['MTR/ATR']=stock_atr_data['MTR']/stock_atr_data['ATR']
    stock_atr_data.to_csv('stock_{}/stock_atr_ratio{}.csv'.format(ts_code,ts_code))
    return stock_atr_data

def get_index_by_callback_proportion(ts_code,start_date,end_date):
    stock_data=get_basic_data(ts_code,start_date,end_date)
    name='CLOSE'
    indexes_peaks, values_peaks = get_line_peaks(stock_data[name])  # 获得所有的峰值点
    indexes_valleys, values_valleys = get_line_valleys(stock_data[name])  # 获得所有的谷值点
    line = stock_data[name].values.tolist()  # 寻找极大值极小值的曲线

    print('数据调整前的峰谷值：')
    print(len(indexes_peaks), indexes_peaks)
    print(len(indexes_valleys), indexes_valleys)
    # 极大值和极小值交替出现，确保峰值在前，谷值在后，序列以峰值开头，以谷值结束
    if (indexes_valleys[0] < indexes_peaks[0]):
        indexes_valleys.pop(0)
    if (indexes_valleys[-1] < indexes_peaks[-1]):
        indexes_peaks.pop()
    print('数据调整后的峰谷值，确保峰值在前，以谷值结束：')
    print(len(indexes_peaks), indexes_peaks)
    print(len(indexes_valleys), indexes_valleys)

    indexes_callback5=[]
    indexes_callback10 = []
    indexes_callback20 = []
    others=[]
    for i in range(len(indexes_peaks)):

        if (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.05:
            indexes_callback5.append(indexes_peaks[i])

        elif (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.1:
            indexes_callback10.append(indexes_peaks[i])

        elif (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.2:
            indexes_callback20.append(indexes_peaks[i])

        else :
            others.append(indexes_peaks[i])

    print('回调5%的点:')
    print(len(indexes_callback5),indexes_callback5)
    print('回调10%的点:')
    print(len(indexes_callback10),indexes_callback10)
    print('回调20%的点')
    print(len(indexes_callback20),indexes_callback20)
    print('回调大于20%的点')
    print(len(others), others)
    stock_data = stock_data.loc[indexes_peaks]
    stock_data.loc[indexes_callback20, 'LABEL'] = 1#二分类
    stock_data.loc[indexes_callback10, 'LABEL'] = 1
    stock_data.loc[indexes_callback5, 'LABEL'] = 0
    stock_data.loc[others, 'LABEL'] = 1
    stock_label_data=stock_data[['TIME', 'LABEL']]
    stock_label_data.to_csv('stock_{}/stock_label_data.csv'.format(ts_code))
    return stock_label_data

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

def weighted_by_boll(tscode,start_date,end_date):
    df0 = get_basic_data(tscode, start_date, end_date)
    df1 = get_boll_data(tscode, start_date, end_date)
    df2= df0.merge(df1)
    line = df2['CLOSE'].tolist()
    line_peaks = []
    indexes_peaks, _ = signal.find_peaks(line, distance=1)  # 获得极大值的index
    for i in indexes_peaks:
        line_peaks.append(line[i])

    df2 = df2.loc[indexes_peaks.tolist()]
    df2['WEIGHT-BY-BOLL'] = np.zeros(len(df2))
    for i in indexes_peaks.tolist():
        if df2.loc[i, 'CLOSE'] < df2.loc[i, 'MID']:
            df2.loc[i, 'WEIGHT-BY-BOLL'] = 0
        elif df2.loc[i, 'CLOSE'] > df2.loc[i, 'MID'] and abs(df2.loc[i, 'CLOSE'] - df2.loc[i, 'UPPER'])/df2.loc[i, 'UPPER'] <= 0.01:
            df2.loc[i, 'WEIGHT-BY-BOLL'] = 1
        elif df2.loc[i, 'CLOSE'] > df2.loc[i, 'MID'] and 0.01<abs(df2.loc[i, 'CLOSE'] - df2.loc[i, 'UPPER'])/df2.loc[i, 'UPPER'] <= 0.02:
            df2.loc[i, 'WEIGHT-BY-BOLL'] = 0.8
        elif df2.loc[i, 'CLOSE'] > df2.loc[i, 'MID'] and 0.02<abs(df2.loc[i, 'CLOSE'] - df2.loc[i, 'UPPER'])/df2.loc[i, 'UPPER'] <= 0.03:
            df2.loc[i, 'WEIGHT-BY-BOLL'] = 0.6
        elif df2.loc[i, 'CLOSE'] > df2.loc[i, 'MID'] and 0.03<abs(df2.loc[i, 'CLOSE'] - df2.loc[i, 'UPPER'])/df2.loc[i, 'UPPER'] <= 0.05:
            df2.loc[i, 'WEIGHT-BY-BOLL'] = 0.4
        elif df2.loc[i, 'CLOSE'] > df2.loc[i, 'MID'] and abs(df2.loc[i, 'CLOSE'] - df2.loc[i, 'UPPER'])/df2.loc[i, 'UPPER']>0.05:
            df2.loc[i, 'WEIGHT-BY-BOLL'] = 0.2
    print('----------------------------------------')
    print('本次抓取的股票{}共有{}天峰值'.format(tscode,len(df2)))
    print('其中收盘价小于中轨线的有{}天'.format(len(df2[df2['WEIGHT-BY-BOLL']==0])))
    print('其中收盘价与上轨线的差值绝对值小于1%的有{}天'.format(len(df2[df2['WEIGHT-BY-BOLL']==1])))
    print('其中收盘价与上轨线的差值绝对值介于1%-2%的有{}天'.format(len(df2[df2['WEIGHT-BY-BOLL']==0.8])))
    print('其中收盘价与上轨线的差值绝对值介于2%-3%的有{}天'.format(len(df2[df2['WEIGHT-BY-BOLL']==0.6])))
    print('其中收盘价与上轨线的差值绝对值介于3%-5%的有{}天'.format(len(df2[df2['WEIGHT-BY-BOLL']==0.4])))
    print('其中收盘价与上轨线的差值绝对值大于5%的有{}天'.format(len(df2[df2['WEIGHT-BY-BOLL']==0.2])))
    #print(df2)
    return df2

def integrate_features(ts_code,start_date,end_date):
    if (os.path.exists('stock_{}/stock_allfactors_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        df2= pd.read_csv('stock_{}/stock_allfactors_{}.csv'.format(ts_code,ts_code),index_col=0)
        print('本次allfactors使用本地数据。')
    else:
        d = get_index_by_callback_proportion(ts_code, start_date, end_date)
        df1 = weighted_by_boll(ts_code, start_date, end_date)
        df1 = df1.loc[d.index]
        df2 = get_some_factors(ts_code, start_date, end_date)
        df2 = df2.loc[d.index]
        df3 = find_atr_market_situation(ts_code, start_date, end_date)
        df3 = df3.loc[d.index]
        kline_type = get_kline_types(ts_code, start_date, end_date)
        kline_type = kline_type.loc[d.index]
        df2['WEIGHT-BY-BOLL']=df1['WEIGHT-BY-BOLL'].values.tolist()
        df2['MTR/ATR']=df3['MTR/ATR'].values.tolist()
        df2['KLINE_TYPE']=kline_type['kline_type'].values.tolist()
        df2['LABEL'] = d['LABEL'].values.tolist()
        # df2.rename(columns={'Unnamed: 0': 'TIME'}, inplace=True)
        df2.to_csv('stock_{}/stock_allfactors_{}.csv'.format(ts_code, ts_code))
        print('本次allfactors重新获取。')

    return df2


if __name__ == "__main__":
    print()

