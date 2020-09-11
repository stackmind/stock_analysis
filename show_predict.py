#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: show_predict.py
@time: 2020/09/08
本部分主要读取训练的模型，并在图上标出所预测的点
分别展示，可通过图例进行筛选
"""
import pandas as pd
import joblib
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from draw_charts import *
import seaborn as sns

def draw_predict_charts(ts_code, start_date, end_date,name):#绘制图表
    stock_data=get_process_datas(ts_code, start_date, end_date)
    x = stock_data['TIME'].values.tolist()
    y = stock_data[name].values.tolist() #收盘价曲线
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
    #极小值的散点图
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
    #收盘价的五日均线
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
    #获取存储的csv文件
    predict_data = pd.read_csv('stock_{}/predict_label.csv'.format(ts_code))
    stock_data=stock_data.set_index('TIME')
    time = predict_data['TIME'].values.tolist()
    #预测值等于实际值的日期
    predict = predict_data['TIME'].where(predict_data['PRE_LABEL'] == predict_data['LABEL']).dropna().tolist()
    predict_close = stock_data.loc[predict]['CLOSE'].values.tolist()
    #预测为1（回调大于5%）且实际也为1的日期
    predict_1 = predict_data['TIME'].where((predict_data['PRE_LABEL']==1) & (predict_data['LABEL']==1)).dropna().tolist()
    predict_1_close=stock_data.loc[predict_1]['CLOSE'].values.tolist()
    # print(predict_1,len(predict_1))
    predict = (
        Scatter()
            .add_xaxis(predict)
            .add_yaxis('预测正确的点', predict_close, label_opts=opts.LabelOpts(is_show=False), symbol='triangle',
                       symbol_rotate=180, itemstyle_opts=opts.ItemStyleOpts(color='#14b143'))
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")], )
    )
    predict_1 = (
        Scatter()
            .add_xaxis(predict_1)
            .add_yaxis('预测正确的且回调大于5%的点', predict_1_close, label_opts=opts.LabelOpts(is_show=False), symbol='triangle',
                       symbol_rotate=180, itemstyle_opts=opts.ItemStyleOpts(color='#14b1ff'))
            .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")], )
    )

    overlap_all = line.overlap(scatter_peak)
    # overlap_all = overlap_all.overlap(scatter_valley)
    overlap_all = overlap_all.overlap(line_boll)
    overlap_all = overlap_all.overlap(line_close)
    overlap_all = overlap_all.overlap(predict)
    overlap_all = overlap_all.overlap(predict_1)

    grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))

    grid_chart.add(
        overlap_all,
        grid_opts=opts.GridOpts(pos_left="25%", pos_right="15%", pos_top="10%"),
    )

    grid_chart.render('stock_{}/stock_predict.html'.format(ts_code))

if __name__ == "__main__":
    ts_code = '300347.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2017-10-01'  # 开始日期
    end_date = '2020-08-31'  # 结束日期
    data = integrate_features(ts_code, start_date, end_date)
    # feature_cols = ['VAL_LNMV', 'RISK_VARIANCE20', 'WEST_NETPROFIT_FY1_1M', 'TECH_REVS5', 'TECH_TURNOVERRATE20',
    #                 'TECH_BEARPOWER', 'TECH_CYF', 'KLINE_TYPE','WEIGHT-BY-BOLL', 'MTR/ATR'
    #                 ]
    feature_cols = ['KLINE_TYPE', 'WEIGHT-BY-BOLL', 'MTR/ATR']
    # 机器学习建模
    X = data[feature_cols]
    y = data['LABEL']

    clf = joblib.load('stock_{}/clf.model'.format(ts_code))
    y_pred = clf.predict(X)

    time = data['TIME'].tolist()
    y = y.tolist()
    y_pred = y_pred.tolist()
    predict_data = pd.DataFrame({'TIME': time, 'LABEL': y, 'PRE_LABEL': y_pred})
    print("Accuracy:", metrics.accuracy_score(y, y_pred))
    print(predict_data)

    predict_data.to_csv('stock_{}/predict_label.csv'.format(ts_code))#把预测的标签和真实标签写入csv文件

    cm = confusion_matrix(y, y_pred)
    # 输出混淆矩阵
    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, cmap='Blues')
    plt.ylim(0, 2)
    plt.xlabel('Predicted lables')
    plt.ylabel('True lables')
    plt.savefig('stock_{}/模型混淆矩阵.png'.format(ts_code))
    plt.show()


    draw_predict_charts(ts_code, start_date, end_date,'CLOSE')
    wb.open('stock_{}\/stock_predict.html'.format(ts_code))
