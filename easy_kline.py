import mplfinance
import tushare as ts
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.pylab import date2num
import numpy as np
'''这里我们对数据按照日期做了个排序，因为tushare默认提供的数据是最新的数据在最前边;
我们用pd.to_datetime()将字符串日期转换为pandas Timestamp格式(类似datetime.datetime)，然后用date2num转换为matplotlib需要的格式。
然后我们另外添加一列dates，这一列用于解决mpl_finance中存在的一些问题，后边我们会详细解释。
'''
sns.set()
pro = ts.pro_api()
df= pro.index_daily(ts_code="000001.SH")
df.head()
df.index = pd.to_datetime(df['trade_date'])
df.index[:5]
fig, ax = plt.subplots(figsize=(10,5))
mplfinance.candlestick_ochl(
    ax=ax,
    quotes=df[['trade_date', 'open', 'close', 'high', 'low']].values,
    width=0.7,
    colorup='r',
    colordown='g',
    alpha=0.7)
ax.xaxis_date()
plt.xticks(rotation=30)


'''所有的节假日包括周末，在这里都会显示为空白，这对于我们图形的连续性非常不友好，因此我们要解决掉他们'''
def format_date(x,pos):
    if x<0 or x>len(date_tickers)-1:
        return ''
    return date_tickers[int(x)]

date_tickers = df.trade_date2.values
fig, ax = plt.subplots(figsize=(10,5))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
mplfinance.candlestick_ochl(
    ax=ax,
    quotes=df[['dates', 'open', 'close', 'high', 'low']].values,
    width=0.7,
    colorup='r',
    colordown='g',
    alpha=0.7)
ax.set_title('上证综指K线图(2018.9-)', fontsize=20);
'''由于matplotlib会将日期数据理解为连续数据，而连续数据之间的间距是有意义的，所以非交易日即使没有数据，在坐标轴上还是会体现出来。连续多少个非交易日，在坐标轴上就对应了多少个小格子，但这些小格子上方并没有相应的蜡烛图。

明白了它的原理，我们就可以对症下药了。我们可以给横坐标（日期）传入连续的、固定间距的数据，先保证K线图的绘制是连续的；然后生成一个保存有正确日期数据的列表，接下来，我们根据坐标轴上的数据去取对应的正确的日期，并替换为坐标轴上的标签即可。

上边format_date函数就是这个作用。由于前边我们给dates列生成了从0开始的序列连续数据，因此我们可以直接把它当作索引，从真正的日期列表里去取对应的数据。在这里我们要使用matplotlib.ticker.FuncFormattter()方法，它允许我们指定一个格式化坐标轴标签的函数，在这个函数里，我们需要接受坐标轴的值以及位置，并返回自定义的标签。
'''