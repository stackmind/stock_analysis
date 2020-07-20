import mpl_finance
import tushare as ts
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.pylab import date2num
import numpy as np
import matplotlib as mpl
sns.set()
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'SimHei'
pro = ts.pro_api()

df = pro.daily(ts_code='000001.SH', start_date='20170101')
df = df.sort_values(by='trade_date', ascending=True)
df['trade_date2'] = df['trade_date'].copy()
df['trade_date'] = pd.to_datetime(df['trade_date']).map(date2num)
df['dates'] = np.arange(0, len(df))
df.head()
df['5'] = df.close.rolling(5).mean()
df['20'] = df.close.rolling(20).mean()
df['30'] = df.close.rolling(30).mean()
df['60'] = df.close.rolling(60).mean()
df['120'] = df.close.rolling(120).mean()
df['250'] = df.close.rolling(250).mean()

def format_date(x,pos):
    if x<0 or x>len(date_tickers)-1:
        return ''
    return date_tickers[int(x)]

date_tickers = df.trade_date2.values
fig, ax = plt.subplots(figsize=(10,5))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
# 绘制K线图
mpl_finance.candlestick_ochl(
    ax=ax,
    quotes=df[['dates', 'open', 'close', 'high', 'low']].values,
    width=0.7,
    colorup='r',
    colordown='g',
    alpha=0.7)
# 绘制均线
for ma in ['5', '20', '30', '60', '120', '250']:
    plt.plot(df['dates'], df[ma])
plt.legend()
ax.set_title('上证综指K线图(2017.1-)', fontsize=20);

df2 = df.query('trade_date2 >= "20180601"').reset_index()
df2['dates'] = np.arange(0, len(df2))
date_tickers = df2.trade_date2.values

fig, ax = plt.subplots(figsize=(10,5))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

# 绘制K线图
mpl_finance.candlestick_ochl(
    ax=ax,
    quotes=df2[['dates', 'open', 'close', 'high', 'low']].values,
    width=0.7,
    colorup='r',
    colordown='g',
    alpha=0.7)

# 绘制均线
for ma in ['5', '20', '30', '60', '120', '250']:
    plt.plot(df2['dates'], df2[ma])
plt.legend()
ax.set_title('上证综指K线图(2018.6-)', fontsize=20);
from matplotlib.gridspec import GridSpec

# 取18.9以来数据
df2 = df.query('trade_date2 >= "20180601"').reset_index()
df2['dates'] = np.arange(0, len(df2))
date_tickers = df2.trade_date2.values

# 控制子图
figure = plt.figure(figsize=(12, 9))
gs = GridSpec(3, 1)
ax1 = plt.subplot(gs[:2, :])
ax2 = plt.subplot(gs[2, :])

# 绘制K线图
mpl_finance.candlestick_ochl(
    ax=ax1,
    quotes=df2[['dates', 'open', 'close', 'high', 'low']].values,
    width=0.7,
    colorup='r',
    colordown='g',
    alpha=0.7)
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

# 绘制均线
for ma in ['5', '20', '30', '60', '120', '250']:
    ax1.plot(df2['dates'], df2[ma])
ax1.legend()
ax1.set_title('上证综指K线图(2018.6-)', fontsize=20)
ax1.set_ylabel('指数')

# 绘制成交量
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
df2['up'] = df.apply(lambda row: 1 if row['close'] >= row['open'] else 0, axis=1)
ax2.bar(df2.query('up == 1')['dates'], df2.query('up == 1')['vol'], color='r', alpha=0.7)
ax2.bar(df2.query('up == 0')['dates'], df2.query('up == 0')['vol'], color='g', alpha=0.7)
ax2.set_ylabel('成交量')
#plt.xticks(date_tickers);
