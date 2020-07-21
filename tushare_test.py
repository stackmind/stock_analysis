import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()#使用seaborn，画图美观
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()#控制futurewaring 报错信息
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号

def show_close_daily(tscode,choose,start_data,end_data):#绘制
    daily_data=pro.daily(ts_code = tscode,start_date = start_data,end_date=end_data)

    #print(daily_data[:1])
    # 转化为日期类型
    daily_data.index= pd.to_datetime(daily_data['trade_date'],format="%Y%m%d")
    daily_data = daily_data.sort_index(ascending=True)#倒序
    # 绘图
    plt.plot(daily_data[choose], '-', label=daily_data.ts_code[0])
    # if choose=='close':
    #     ma=daily_data[choose].rolling(10).mean()#若选项为收盘价，绘制10日均线
    #     plt.plot(ma,'-',label='10日均线')
#ts.set_token('a52a8119d78a018a4559c35a64866ec6f46feb44ab26f59837a0555d')#注册获取token
pro = ts.pro_api()
ts_codes=['300529.SZ','600600.SH'] #此处填写股票号'688399.SH','300347.SZ',
start_data = '20170101' #开始日期
end_data='20200717' #结束日期
choose='close' #可选绘图参数
figure = plt.figure(figsize=(18, 10))
for ts_code in ts_codes:
    show_close_daily(ts_code,choose,start_data,end_data)

plt.gcf().autofmt_xdate()  # 自动旋转日期标记
# 显示文字
plt.legend()
plt.title('{0}走势图{1}-{2}'.format(choose,start_data,end_data))
# 显示图片
plt.show()
