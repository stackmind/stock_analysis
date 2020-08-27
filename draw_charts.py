#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:shihaojie
@file: draw_charts.py
@time: 2020/08/27
"""
from get_stock_data import *
from get_train_factors import *
from pyecharts.charts import Page, Kline, Bar, Grid, Line,Scatter
from pyecharts import options as opts
import webbrowser as wb
from pyecharts.commons.utils import JsCode
def get_process_datas(ts_code, start_date, end_date):#合并获得的数据
    if (os.path.exists('stock_{}/stock_{}.csv'.format(ts_code,ts_code))):  # 判断本地是否存在文档，若没有则调用接口
        # 将数据保存到本地csv文件
        stock_data = pd.read_csv('stock_{}/stock_{}.csv'.format(ts_code,ts_code),index_col=0)
        print('本次使用本地数据。')
    else:
        stock_basic_data = get_basic_data(ts_code, start_date, end_date)
        stock_kdj_data = get_kdj_data(ts_code, start_date, end_date)
        stock_ma_data = get_ma_data(ts_code, start_date, end_date)
        stock_macd_data = get_macd_data(ts_code, start_date, end_date)
        stock_boll_data = get_boll_data(ts_code, start_date, end_date)
        stock_data = pd.merge(stock_basic_data,stock_ma_data)
        stock_data = pd.merge(stock_data,stock_kdj_data)
        stock_data = pd.merge(stock_data,stock_macd_data)
        stock_data = pd.merge(stock_data,stock_boll_data)
        stock_data.to_csv('stock_{}/stock_{}.csv'.format(ts_code,ts_code))
        print('本次数据从Windpy网络获取。')
    return stock_data
def draw_chart(ts_code, start_date, end_date):
    '''
        pyecharts V1 版本开始支持链式调用
       文档地址 https://pyecharts.org/#/zh-cn/
    '''
    stock_data=get_process_datas(ts_code, start_date, end_date)
    stock_data.index = pd.to_datetime(stock_data['TIME'], format="%Y/%m/%d")
    x = stock_data["TIME"].values.tolist()
    stock_basic_data = stock_data[["TIME", "OPEN", "CLOSE", "LOW", "HIGH", "VOLUME"]]
    # stock_data = stock_data.sort_index(ascending=True)  # 倒序，看时间顺序是否正常决定是不是要用
    # k线图
    kline = (
        Kline()
            .add_xaxis(x)
            .add_yaxis("K线图", stock_basic_data.iloc[:, 1:5].values.tolist(), itemstyle_opts=opts.ItemStyleOpts(
            color="#ec0000",
            color0="#00da3c"
        ),)
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
            title_opts=opts.TitleOpts(title="股票价格",
                                      subtitle=ts_code,
                                      pos_left='22%',
                                      pos_top="20%"),
            #把所有的x轴连接在一起
            # axispointer_opts=opts.AxisPointerOpts(is_show=True,
            #                                       link=[{"xAxisIndex": "all"}],
            #                                       label=opts.LabelOpts(background_color="#777"),
            #                                       ),

            datazoom_opts=[  # 设置zoom参数后即可缩放
                opts.DataZoomOpts(
                    is_show=True,
                    type_="inside",
                    xaxis_index=[0,1,2,3,4],  # 设置第0轴和第1轴同时缩放
                    range_start=0,
                    range_end=100,
                ),

            ],

        )
    )
    # 成交量柱形图
    bar_volumn = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("成交量",
                       stock_basic_data["VOLUME"].values.tolist(),
                       xaxis_index=1,
                       yaxis_index=1,
                       label_opts=opts.LabelOpts(is_show=False),
                       itemstyle_opts=opts.ItemStyleOpts(
                           color=JsCode(
                               """
                           function(params) {
                               var colorList;
                               if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                                   colorList = '#ef232a';

                               } else {
                                   colorList = '#14b143';
                               }
                               return colorList;
                           }
                           """
                           )
                       ),
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title="成交量", pos_left='22%',pos_top="48%"),
                             legend_opts=opts.LegendOpts(is_show=True,orient='vertical',pos_right="5%",pos_top='48%'),
                             )
    )
    #绘制均线图
    line_ma = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="MA5",
            y_axis=stock_data["MA5"].values.tolist(),

            is_hover_animation=False,
            # linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="MA10",
            y_axis=stock_data["MA10"].values.tolist(),

            is_hover_animation=False,

            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="MA20",
            y_axis=stock_data["MA20"].values.tolist(),

            is_hover_animation=False,

            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )

            .set_global_opts(title_opts=opts.TitleOpts(title="MA", pos_left='22%', pos_top="88%"),
                             xaxis_opts=opts.AxisOpts(type_="category",axislabel_opts=opts.LabelOpts(is_show=False),is_scale=True),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside")],
                             legend_opts=opts.LegendOpts(is_show=True,orient='vertical',pos_right="5%",pos_top='85%'),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),)
    )
#绘制jdk线
    line_kdj = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="K",
            y_axis=stock_data["K"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="D",
            y_axis=stock_data["D"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="J",
            y_axis=stock_data["J"].values.tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )

            .set_global_opts(title_opts=opts.TitleOpts(title="KDJ", pos_left='22%',pos_top="62%"),
                             datazoom_opts=[opts.DataZoomOpts(type_="inside",)],
                             legend_opts=opts.LegendOpts(is_show=True,orient='vertical',pos_right="7%",pos_top='60%'),
                             xaxis_opts=opts.AxisOpts(is_scale=True,axislabel_opts=opts.LabelOpts(is_show=False),),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),

                             )
    )
    #绘制macd柱状图
    bar_macd=(
        Bar().add_xaxis(x)
        .add_yaxis(series_name='MACD',
                   yaxis_data=stock_data['MACD'].values.tolist(),
                   xaxis_index=2,
                   yaxis_index=2,
                   label_opts=opts.LabelOpts(is_show=False),
                   itemstyle_opts=opts.ItemStyleOpts(
                       color=JsCode(
                           """
                               function(params) {
                                   var colorList;
                                   if (params.data >= 0) {
                                     colorList = '#ef232a';
                                   } else {
                                     colorList = '#14b143';
                                   }
                                   return colorList;
                               }
                               """
                       )
                   ),
                   )
                   .set_global_opts(
                    title_opts=opts.TitleOpts(title="MACD", pos_left='22%', pos_top="75%"),
                    xaxis_opts=opts.AxisOpts(
                    type_="category",
                    grid_index=2,
                    axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=2,
                split_number=4,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=True),
            ),
            legend_opts=opts.LegendOpts(is_show=True,orient='vertical',pos_right="5%",pos_top='70%'),
        )
    )
    #绘制DIF和DEA
    line_macd = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="DIF",
            y_axis=stock_data['DIF'].values.tolist(),
            xaxis_index=2,
            yaxis_index=2,
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="DEA",
            y_axis=stock_data['DEA'].values.tolist(),
            xaxis_index=2,
            yaxis_index=2,
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show=False,
        )
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    )
    #绘制布林线
    line_boll = (
        Line()
            .add_xaxis(x)
            .add_yaxis(
            series_name="MID",
            y_axis=stock_data["MID"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="UPPER",
            y_axis=stock_data["UPPER"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )
            .add_yaxis(
            series_name="LOWER",
            y_axis=stock_data["LOWER"].values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            is_symbol_show = False,
        )

            .set_global_opts(
                             datazoom_opts=[opts.DataZoomOpts(type_="inside", )],

                             xaxis_opts=opts.AxisOpts(is_scale=True),
                             yaxis_opts=opts.AxisOpts(
                                 is_scale=True,
                                 splitarea_opts=opts.SplitAreaOpts(
                                     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                 ),
                             ),)
    )



    overlap_kline_linema= kline.overlap(line_boll)
    overlap_macd=bar_macd.overlap(line_macd)
    # 使用网格将多张图标组合到一起显示
    grid_chart = Grid(init_opts=opts.InitOpts(
        width="1400px",
        height="700px",
        animation_opts=opts.AnimationOpts(animation=False),
    ))

    # 为了把 data.datas 的数据写入到html中作为全局变量,目前无法跨 series 传值
    # demo 中的代码也是用全局变量传的
    grid_chart.add_js_funcs("var barData = {}".format(stock_basic_data.iloc[:, 1:5].values.tolist()))
    grid_chart.add(
        overlap_kline_linema ,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="3%",height="40%"),

    )

    grid_chart.add(
        bar_volumn,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="45%", height="10%"),
    )

    grid_chart.add(
        line_kdj,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="60%", height="10%")
    )
    grid_chart.add(
        overlap_macd,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="72%", height="10%")
    )

    grid_chart.add(
        line_ma,
        grid_opts=opts.GridOpts(pos_left="35%", pos_right="15%", pos_top="85%", height="10%")
    )

    grid_chart.render('stock_{}/stock_{}.html'.format(ts_code,ts_code))  # 保存成用股票代码命名的文档
    return 0

def draw_peak_charts(ts_code, start_date, end_date,name):
    stock_data=get_process_datas(ts_code, start_date, end_date)
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
if __name__ == "__main__":
    ts_code = '300347.SZ'  # 此处填写股票号'688399.SH','300347.SZ',
    start_date = '2017-09-01'  # 开始日期
    end_date = '2020-08-01'  # 结束日期
    draw_chart(ts_code, start_date, end_date)
    draw_peak_charts(ts_code, start_date, end_date,'CLOSE')
