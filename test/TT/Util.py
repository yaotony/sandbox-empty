import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np

def drawMap(KBar1M,df,filename,orderValue,note =None) :
    FastPeriod=10
    SlowPeriod=30 
    
    KData = KBar1M.GetChartTypeData()
    df = df.sort_values(by=['time'],ascending=True)
    #FastMA=KBar1M.GetMAByOpen(FastPeriod,0)
    #B40MA=KBar1M.GetMAByOpen(SlowPeriod,0)
    FastMA=df['ma_s']
    SlowMA=df['ma_l']
    ma_40=df['ma_40']

    BoxTop =  df['BoxTop'] 
    BoxDown =df['BoxDown'] 
    Prices=orderValue['Price']

    Time=KBar1M.GetTime()    
    #定義圖表物件
   # zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\mingliu.ttf')
    #plt.legend(prop=zhfont1)
    plt.rcParams['font.sans-serif'] = ['mingliu']
    plt.rcParams['axes.unicode_minus'] = False
    #plt.rcParams['savefig.dpi'] = 200 #图片像素
    #plt.rcParams['figure.dpi'] = 200 #分辨率
  
    
    ax = plt.subplot(111)
    #繪製圖案 ( 圖表 , K線物件 )
    candlestick_ohlc(ax, KData, width=0.0003, colorup='r', colordown='g')  
    ax.plot_date( Time,FastMA, 'k-' , linewidth=1 ,color='#00FFFF')
    ax.plot_date( Time,SlowMA, 'k-' , linewidth=1 ,color='#FFFF00')
    ax.plot_date( Time,BoxTop, 'k-' , linewidth=1 ,color='#0000FF')
    ax.plot_date(Time ,ma_40, 'k-' , linewidth=1 ,color='#FF0000')
    ax.plot_date( Time,BoxDown, 'k-' , linewidth=1 ,color='#00FF00')
    for i in  range( len(orderValue)):
        
        if orderValue['BC'].iloc[i] == -1 :
            ax.annotate( str(orderValue['Price'].iloc[i])+orderValue['note'].iloc[i] , xy=(Time[i], Prices[i]), xytext=(Time[i], Prices[i]),
                xycoords='data',
                arrowprops=dict(facecolor='green', shrink=0.05)
                )
        elif orderValue['BC'].iloc[i]== 1 :
            ax.annotate(str(orderValue['Price'].iloc[i])+orderValue['note'].iloc[i], xy=(Time[i], Prices[i]), xytext=(Time[i], Prices[i]),
                xycoords='data',
                arrowprops=dict(facecolor='red', shrink=0.05)
                )

    # X軸的間隔設為半小時
    plt.xticks(np.arange(KData[0][0],KData[-1][0], 1/1440*30))
        
    #定義標頭
    ax.set_title(note)

    #定義x軸
    hfmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(hfmt)
    plt.savefig('C:\\Temp\\'+filename+'.png')#儲存圖片
    #顯示繪製圖表
    plt.show()       
    # #定義圖表物件
    # ax = plt.subplot(111)
    # plt.rcParams['font.sans-serif'] = ['PingFang HK']

    # ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    # #繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    # ax.plot_date( Time,BoxTop, 'k-' , linewidth=1 ,color='#0000FF')
    # ax.plot_date( Time,Price, 'k-' , linewidth=1 ,color='#FF0000')
    # ax.plot_date( Time,BoxDown, 'k-' , linewidth=1 ,color='#00FF00')
    # for i in  range( len(mmData)):
    #     if mmData['sign'].iloc[i] == -1 :
    #         ax.annotate(NoteText[i], xy=(Time[i], Price[i]), xytext=(Time[i], Price[i]),
    #             xycoords='data',
    #             arrowprops=dict(facecolor='green', shrink=0.05)
    #             )
    #     elif mmData['sign'].iloc[i]== 1 :
    #         ax.annotate(NoteText[i], xy=(Time[i], Price[i]), xytext=(Time[i], Price[i]),
    #             xycoords='data',
    #             arrowprops=dict(facecolor='red', shrink=0.05)
    #             )

    #     elif  len(mmData['note'].iloc[i]) > 0:
    #         ax.annotate(NoteText[i], xy=(Time[i], Price[i]), xytext=(Time[i], Price[i]),
    #             xycoords='data',
    #             arrowprops=dict(facecolor='fuchsia', shrink=0.05)
    #             )
        



    # #定義標頭
    # ax.set_title(title)

    # #定義x軸
    # hfmt = mdates.DateFormatter('%H:%M')
    # ax.xaxis.set_major_formatter(hfmt)

    # table = pd.plotting.table(ax, result, loc='bottom')
    # table.set_fontsize(14)
    # table.scale(1.5, 1.5)  # may help
    # #顯示繪製圖表
    # plt.show()