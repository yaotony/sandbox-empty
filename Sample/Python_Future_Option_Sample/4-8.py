# -*- coding: utf-8 -*-

# 載入必要套件
from indicator import GetHistoryData,KBar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import datetime,sys
strptime=datetime.datetime.strptime
import numpy as np

# 取得資料
# Date='20190902'
# Product='TXFI9'
Date=sys.argv[1]
Product=sys.argv[2]
FilePath='C:/Data/'
Broker='Simulator'
Table='Match'
Data=GetHistoryData(FilePath,Broker,Date,Product,Table)

# 取特定時間的資料
Data = [ line for line in Data if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' ]

# 定義1分K棒的物件
MinuteKBar=KBar(Date,1)
# 計算K棒
for line in Data:
    time=strptime(line[0],"%Y/%m/%d %H:%M:%S.%f")
    price=int(line[2])
    qty=int(line[3])
    MinuteKBar.AddPrice(time,price,qty)

KData=MinuteKBar.GetChartTypeData()

#定義圖表物件
ax = plt.subplot(111)

#繪製圖案 ( 圖表 , K線物件 )
candlestick_ohlc(ax, KData, width=0.0003, colorup='r', colordown='g')  

# X軸的間隔設為半小時
plt.xticks(np.arange(KData[0][0],KData[-1][0], 1/1440*30))
    
#定義標頭
ax.set_title('OHLC')

#定義x軸
hfmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hfmt)

#顯示繪製圖表
plt.show()



