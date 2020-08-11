#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:shihaojie
@file: find_peak.py
@time: 2020/08/3
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from stock_analysis import get_process_datas,find_daily_situation
from pyecharts.charts import Line,Grid,Scatter,Kline
from pyecharts import options as opts
import webbrowser as wb
import pandas as pd

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

def draw_charts(stock_data,name):

    x = stock_data['TIME'].values.tolist()
    y = stock_data[name].values.tolist()
    indexes_peaks, line_peaks=get_line_peaks(stock_data[name])
    indexes_valleys, line_valleys=get_line_valleys(stock_data[name])

    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis('收盘价', y, label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False, )
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")],
                             title_opts=opts.TitleOpts(title="股票价格",
                                                       subtitle=ts_code,
                                                       pos_left='15%',
                                                       pos_top="40%"),
                             # 把所有的x轴连接在一起
                             axispointer_opts=opts.AxisPointerOpts(is_show=True,
                                                                   link=[{"xAxisIndex": "all"}],
                                                                   label=opts.LabelOpts(background_color="#777"),
                                                                   ),

                             )

    )

    # 极大值的散点图
    scatter_peak = (
        Scatter()
            .add_xaxis(indexes_peaks)
            .add_yaxis('Peaks', line_peaks, label_opts=opts.LabelOpts(is_show=False), symbol='triangle',
                       symbol_rotate=180, itemstyle_opts=opts.ItemStyleOpts(color='#ef232a'))
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")], )
    )

    scatter_valley = (
        Scatter()
            .add_xaxis(indexes_valleys)
            .add_yaxis('Valleys', line_valleys, label_opts=opts.LabelOpts(is_show=False), symbol='triangle',
                       itemstyle_opts=opts.ItemStyleOpts(color='#14b143'))
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")], )
    )
    #绘制布林带
    line_boll = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="MID",
            y_axis=stock_data["MID"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False,
        )
            .add_yaxis(
            series_name="UPPER",
            y_axis=stock_data["UPPER"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False,
        )
            .add_yaxis(
            series_name="LOWER",
            y_axis=stock_data["LOWER"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False,
        )

            .set_global_opts(datazoom_opts=[opts.DataZoomOpts(type_="inside", )],
                             xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ), )
    )

    stock_basic_data = stock_data[["TIME", "OPEN", "CLOSE", "LOW", "HIGH"]]
    # 绘制K线图
    kline = (
        Kline()
            .add_xaxis(x)
            .add_yaxis("K线图", stock_basic_data.iloc[:, 1:5].values.tolist(), itemstyle_opts=opts.ItemStyleOpts(
            color="#ec0000",
            color0="#00da3c"
        ), )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True,
                                     is_show=False),
            # axis_opts=opts.AxisOpts(is_scale=True,min_=0), #y轴起始坐标可以设为0
            yaxis_opts=opts.AxisOpts(is_scale=True,
                                     splitarea_opts=opts.SplitAreaOpts(is_show=True,
                                                                       areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                                                       ),
                                     ),  # y轴起始坐标可自动调整
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
            legend_opts=opts.LegendOpts(is_show=True, orient='vertical', pos_right="5%", pos_top='20%'),

            datazoom_opts=[  # 设置zoom参数后即可缩放
                opts.DataZoomOpts(
                    is_show=True,
                    type_="inside",

                ),

            ],

        )
    )
    line_close = (
        Line()
            .add_xaxis(x)
            .add_yaxis('五日均线', stock_data["MA5"].values.tolist(), label_opts=opts.LabelOpts(is_show=False),
                       is_symbol_show=False, )
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")],
                             )

    )
    overlap_findpeak = line.overlap(scatter_peak)
    overlap_findpeak = overlap_findpeak.overlap(scatter_valley)
    overlap_findpeak = overlap_findpeak.overlap(line_boll)
    overlap_findpeak = overlap_findpeak.overlap(kline)
    overlap_findpeak = overlap_findpeak.overlap(line_close)

    grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))

    grid_chart.add(
        overlap_findpeak,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

    grid_chart.render('stock_{}/find_peak.html'.format(ts_code))

def show_index_by_boll(stock_data,indexes):

    upper = stock_data['UPPER'].values.tolist()
    mid = stock_data['MID'].values.tolist()
    lower = stock_data['LOWER'].values.tolist()
    line = stock_data['MA5'].values.tolist()  # 寻找极大值极小值的曲线
    index_above_upper = []  # 在布林线上轨之上的点的index
    index_between_mid_and_upper = []  # 在布林线上轨和中轨之间的点的index
    index_between_mid_and_lower = []  # 在布林线中轨和下轨之间的点的index
    index_below_lowwer = []  # 在布林线下轨之下的点的index

    for i in indexes:
        if line[i] >= upper[i]:
            index_above_upper.append(i)
        elif line[i] >= mid[i]:
            index_between_mid_and_upper.append(i)
        elif line[i] >= lower[i]:
            index_between_mid_and_lower.append(i)
        else:
            index_below_lowwer.append(i)

    print('在布林线上轨上的点：',len(index_above_upper), index_above_upper)
    print('在布林线上轨中轨间的点：',len(index_between_mid_and_upper), index_between_mid_and_upper)
    print('在布林线中轨下轨间的点：',len(index_between_mid_and_lower), index_between_mid_and_lower)
    print('在布林线下轨下的点：',len(index_below_lowwer), index_below_lowwer)

def get_index_by_boll(stock_data,name):

    indexes_peaks, values_peaks = get_line_peaks(stock_data[name])  # 获得所有的峰值点
    indexes_valleys, values_valleys = get_line_valleys(stock_data[name])  # 获得所有的谷值点

    show_index_by_boll(stock_data, indexes_peaks)  # 查看峰值点的分布
    print('-' * 50)
    show_index_by_boll(stock_data, indexes_valleys)  # 查看谷值点的分布
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

    mid = stock_data['MID'].values.tolist()
    line = stock_data[name].values.tolist()  # 寻找极大值极小值的曲线

    peaks_callback_from_upper_to_lower = []  # 从布林线中轨以上回调到中轨以下的峰值index
    peaks_callback_between_mid_and_upper = []  # 在布林线中轨以上回调的峰值index
    peaks_callback_between_mid_and_lower = []  # 在布林线中轨以下回调的峰值index

    valleys_callback_from_upper_to_lower = []  # 从布林线中轨以上回调到中轨以下的谷值index
    valleys_callback_between_mid_and_upper = []  # 在布林线中轨以上回调的谷值index
    valleys_callback_between_mid_and_lower = []  # 在布林线中轨以下回调的谷值index


    for i in range(len(indexes_peaks)):
        if (line[indexes_peaks[i]] >= mid[indexes_peaks[i]]) and (line[indexes_valleys[i]] >= mid[indexes_valleys[i]]):
            peaks_callback_between_mid_and_upper.append(indexes_peaks[i])
            valleys_callback_between_mid_and_upper.append(indexes_valleys[i])

        elif (line[indexes_peaks[i]] >= mid[indexes_peaks[i]]) and (line[indexes_valleys[i]] < mid[indexes_valleys[i]]):
            peaks_callback_from_upper_to_lower.append(indexes_peaks[i])
            valleys_callback_from_upper_to_lower.append(indexes_valleys[i])

        elif (line[indexes_peaks[i]] < mid[indexes_peaks[i]]) and (line[indexes_valleys[i]] < mid[indexes_valleys[i]]):
            peaks_callback_between_mid_and_lower.append(indexes_peaks[i])
            valleys_callback_between_mid_and_lower.append(indexes_valleys[i])

        else:
            print('有异常点',indexes_peaks[i])
    print('在布林线中轨以上回调的峰谷值:')
    print(peaks_callback_between_mid_and_upper)
    print(valleys_callback_between_mid_and_upper)
    print('在布林线中轨以上回调到中轨以下的峰谷值:')
    print(peaks_callback_from_upper_to_lower)
    print(valleys_callback_from_upper_to_lower)
    print('在布林线中轨以下回调的峰谷值:')
    print(peaks_callback_between_mid_and_lower)
    print(valleys_callback_between_mid_and_lower)
    return peaks_callback_from_upper_to_lower ,peaks_callback_between_mid_and_upper,peaks_callback_between_mid_and_lower

def get_index_by_callback_proportion(stock_data,name):
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

    indexes_callback10=[]
    indexes_callback20 = []
    indexes_callback30 = []
    temp=[]
    for i in range(len(indexes_peaks)):

        if (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.1:
            indexes_callback10.append(indexes_peaks[i])

        elif  (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.2:
            indexes_callback20.append(indexes_peaks[i])

        elif (line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]]<=0.3:
            indexes_callback30.append(indexes_peaks[i])

        else :
            print('有异常点。')
        temp.append((line[indexes_peaks[i]]-line[indexes_valleys[i]])/line[indexes_peaks[i]])
    print(len(temp),temp)
    print('回调10%的点:')
    print(len(indexes_callback10),indexes_callback10)
    print('回调20%的点:')
    print(len(indexes_callback20),indexes_callback20)
    print('回调30%的点')
    print(len(indexes_callback30),indexes_callback30)
    print(stock_data.loc[indexes_callback20])
    print(stock_data.loc[indexes_callback30])

    return indexes_callback30,indexes_callback20,indexes_callback10

def mark_by_boll(stock_data):

    peaks_callback_from_upper_to_lower, \
    peaks_callback_between_mid_and_upper, \
    peaks_callback_between_mid_and_lower=get_index_by_boll(stock_data,'CLOSE')  #获取不同分类点的index

    df1=stock_data.loc[peaks_callback_from_upper_to_lower]
    df2=stock_data.loc[peaks_callback_between_mid_and_upper]
    df3=stock_data.loc[peaks_callback_between_mid_and_lower]
    # print(stock_data.loc[767])
    df1['LABEL']=0
    df2['LABEL']=1
    df3['LABEL']=2
    frames=[df1,df2,df3]
    result = pd.concat(frames)
    result.to_csv('stock_{}/peaks_result.csv'.format(ts_code))

def mark_peaks_by_31situation(stock_data,name):
    indexes_peaks, values_peaks = get_line_peaks(stock_data[name])#股票所有数据中峰值点的index和值
    data = find_daily_situation(ts_code, start_date, end_date)#股票所有数据中符合三阴一阳和三阴一阴的点的日期
    indexes_data=stock_data[stock_data.loc[:,'TIME'].isin(data)].index.tolist()#股票所有数据中日期符合三阴一阳和三阴一阴的点的index
    # print(len(data),data)
    # print(len(indexes_data),indexes_data)
    weights1=[]
    weights2=[]
    weights3=[]
    weights4=[]
    for i in indexes_peaks:
        if i in indexes_data:
            weights1.append(i)
        elif (i-1) in indexes_data or (i+1) in indexes_data:
            weights2.append(i)
        elif (i-2) in indexes_data or (i+2) in indexes_data:
            weights3.append(i)
        else:
            weights4.append(i)
    # print(len(weights1),weights1)
    # print(len(weights2), weights2)
    # print(len(weights3), weights3)
    # print(len(weights4), weights4)
    stock_data=stock_data.loc[indexes_peaks]
    stock_data['situation'] = 0
    # print(stock_data[:10])
    # print(stock_data.loc[data])
    stock_data.loc[weights1, 'situation'] = 1
    stock_data.loc[weights2, 'situation'] = 0.5
    stock_data.loc[weights3, 'situation'] = 0.2

    stock_data.to_csv('test.csv')


def MaxDrawdown(return_list):
    '''最大回撤率'''
    i = np.argmax((np.maximum.accumulate(return_list) - return_list) / np.maximum.accumulate(return_list))  # 结束位置
    if i == 0:
        return 0
    j = np.argmax(return_list[:i])  # 开始位置
    return (return_list[j] - return_list[i]) / (return_list[j])


if __name__ == '__main__':
    ts_code = '300347.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2017-08-10'  # 开始日期
    end_date = '2020-08-01'  # 结束日期
    stock_data=get_process_datas(ts_code, start_date, end_date)
    # print(stock_data.head())
    draw_charts(stock_data,'CLOSE')
    wb.open('stock_{}\/find_peak.html'.format(ts_code))

    # return_list=stock_data['CLOSE'].values.tolist()
    # print('最大回撤率：',MaxDrawdown(return_list))

    get_index_by_callback_proportion(stock_data,'CLOSE')
    mark_peaks_by_31situation(stock_data,'CLOSE')

















