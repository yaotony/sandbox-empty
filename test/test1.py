from indicator import GetHistoryData,KBar
from Strategy5 import BoxTheory as BT
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime,sys
strptime=datetime.datetime.strptime

from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter
import time 
import requests,datetime,os

from DataConn import getDBData,getDBDataForWebAPI
from LineMSG import linePush









    




#計算各項策略績效指標
#df為欲分析策略績效的資料
def result_F(df,v,n):
    #計算最後報酬
    last = int( df['cus'].iloc[-1])
    #計算交易次數
    count = int( df['sign'][df['sign']!=0].count())
    wamt =int( df['ret'][df['ret']>0].sum())
    lamt =int( df['ret'][df['ret']<0].sum())
    
    #計算最大回檔
    def maxdrawdown(s):
        s = s.cummax() - s #歷史最高價 - 現在序列,cummax 生成當日之前的歷史最高價序列
        return (s.max())
    
    mdd =int( maxdrawdown(df['cus']))
    #計算勝率
    #若交易次數=0，則勝率=0
    if count == 0 :
        w = 0
    else :
        w = df['ret'][df['ret']>0].count() / count 
    #將最後報酬、交易次數、最大回檔、勝率，統整成表格
    result = pd.DataFrame({
        '最後報酬':[last],
        '總賺錢點數':[wamt],
        '總賠錢點數':[lamt],
        '交易次數':[count],
        '最大回檔':[mdd],
        '勝率':[w]
    })
     
    v.append([n,last,wamt,lamt,count,mdd,w])

    return(result)

#輸出回測結果到Excel 檔案
#mane為指定輸出excel檔案名稱，df為輸出資料內容，result 為績效指標
#k為保留k線數，L為總資料筆數
def out_excle(name,df,result) :
    writer = pd.ExcelWriter('/Users/Tony/Downloads/'+ name+'.xlsx',engine=None)
    df.to_excel(writer,'0') #將df資料輸出到 '0' 工作表
    result.to_excel(writer,'result') #將result資料輸出到 'result' 工作表
    #將df['cus']資料輸出到'result'工作表，指定第5欄輸出
    #df['cus'].to_excel(writer,'result',startcol=5)
   
    writer.save()

def out_ResultExcle(filePath,name,allResult) :
    writer = pd.ExcelWriter(filePath+'/'+ name+'.xlsx',engine=None)
    allResult.to_excel(writer,'result') #將result資料輸出到 'result' 工作表
    writer.save()

def drawMap(df ,title ,result) :
    mmData = df
    #取得轉換時間字串至時間格式
    Time = mmData['Time'].iloc[:]
    #價格由字串轉數值
    Price = mmData['Close'].iloc[:]

    NoteText = mmData['note'].iloc[:]
   

    #BoxTop	BoxDown
    BoxTop   = mmData['BoxTop'].iloc[:]
    BoxDown  = mmData['BoxDown'].iloc[:]

    #定義圖表物件
    ax = plt.subplot(111)
    plt.rcParams['font.sans-serif'] = ['PingFang HK']

    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    #繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    ax.plot_date( Time,BoxTop, 'k-' , linewidth=1 ,color='#0000FF')
    ax.plot_date( Time,Price, 'k-' , linewidth=1 ,color='#FF0000')
    ax.plot_date( Time,BoxDown, 'k-' , linewidth=1 ,color='#00FF00')
    for i in  range( len(mmData)):
        if mmData['sign'].iloc[i] == -1 :
            ax.annotate(NoteText[i], xy=(Time[i], Price[i]), xytext=(Time[i], Price[i]),
                xycoords='data',
                arrowprops=dict(facecolor='green', shrink=0.05)
                )
        elif mmData['sign'].iloc[i]== 1 :
            ax.annotate(NoteText[i], xy=(Time[i], Price[i]), xytext=(Time[i], Price[i]),
                xycoords='data',
                arrowprops=dict(facecolor='red', shrink=0.05)
                )

        elif  len(mmData['note'].iloc[i]) > 0:
            ax.annotate(NoteText[i], xy=(Time[i], Price[i]), xytext=(Time[i], Price[i]),
                xycoords='data',
                arrowprops=dict(facecolor='fuchsia', shrink=0.05)
                )
        



    #定義標頭
    ax.set_title(title)

    #定義x軸
    hfmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(hfmt)

    table = pd.plotting.table(ax, result, loc='bottom')
    table.set_fontsize(14)
    table.scale(1.5, 1.5)  # may help
    #顯示繪製圖表
    plt.show()




# 讀取資料  /Users/Tony/Downloads/TX
#df = pd.read_csv('/Users/Tony/Downloads/abc_27.csv',encoding="UTF8")

DataPath='/Users/Tony/Downloads'
Broker='TX'

FilePath=DataPath+'/'+Broker+'/'
# 找出在資料夾中的日期
filenames=[ day for day in os.listdir(FilePath) if day.find('csv') >=0 ]
filenames.sort()
# 定義要回傳的List

    # 透過迴圈將每天的檔案都放進該迴圈中

columns =['日期','最後報酬','總賺錢點數','總賠錢點數','交易次數','最大回檔','勝率']
reValues =[]
   

starTime = datetime.datetime.strptime('2021-02-17 09:00:00','%Y-%m-%d %H:%M:%S')
endTime = datetime.datetime.strptime('2021-02-17 09:00:00','%Y-%m-%d %H:%M:%S')
endTimeTest = datetime.datetime.strptime('2021-02-17 13:30:00','%Y-%m-%d %H:%M:%S')

#df = getDBDataForWebAPI(starTime,endTimeTest)
#BT(df,5,1)
#df['cus'] = df['ret'].cumsum()
#result = result_F(df,reValues,'DB1')
#out_excle('DB1',df,result)
#drawMap(df,'DB1',result)
#linemsg =result.columns[0] +":"+str(result[result.columns[0]].iloc[0]) +',' +result.columns[1] +":"+str(result[result.columns[1]].iloc[0]) +',' +result.columns[2] +":"+str(result[result.columns[2]].iloc[0])+',' +result.columns[3] +":"+str(result[result.columns[3]].iloc[0])+',' +result.columns[4] +":"+str(result[result.columns[4]].iloc[0])+',' +result.columns[5] +":"+str(result[result.columns[5]].iloc[0])
#linePush( linemsg)

for i in range (len(filenames)):
    df =   pd.read_csv(FilePath+filenames[i],encoding="UTF8")
    #Strategy1  
    #BT(df,5,5)
    #Strategy2  
    BT(df,5,1)
    #計算累計損益
    df['cus'] = df['ret'].cumsum()
    result = result_F(df,reValues,filenames[i])
    out_excle(filenames[i],df,result)
    #drawMap(df,filenames[i],result)
  
    #計算各項策略績效指標





nowTime = int(time.time()) # 取得現在時間
struct_time = time.localtime(nowTime) # 轉換成時間元組
timeString = time.strftime("%Y%m%d%I%M%S%P", struct_time) # 將時間元組轉換成想要的字串
reDF = pd.DataFrame(reValues, columns = columns)
#print(reDF)
out_ResultExcle(FilePath,timeString,reDF)

