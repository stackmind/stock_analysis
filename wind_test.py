import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime,time
import os
#from Windpy import *
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号


stock_data=pd.read_csv('300529.csv',encoding = 'gb2312')
stock_data['日期'] = pd.to_datetime(stock_data['日期'])
stock_data.set_index(stock_data['日期'],inplace=True)
print(stock_data[:5])
print(stock_data.info())
print(stock_data.describe())
figure = plt.figure(figsize=(18,10))
stock_data['收盘价'].plot(legend = True)

plt.show()