from indicator import getFutureDailyInfo
from indicator import KBar
import pandas as pd
import time ,datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
from LineMSG import send_message

import math
import numpy as np
from Order2 import inp,outp,stop,stopByMA
from Strategy6 import BoxTheory
import os


def saveDrawMap(KBar1M,df,filename,note =None) :
    FastPeriod=10
    SlowPeriod=30 
    KData = KBar1M.GetChartTypeData()
    df = df.sort_values(by=['time'],ascending=True)
    FastMA=KBar1M.GetMAByOpen(FastPeriod,0)
    SlowMA=KBar1M.GetMAByOpen(SlowPeriod,0)
    BoxTop =   df['BoxTop'] 
    BoxDown =df['BoxDown'] 

    Time=KBar1M.GetTime()    
    #定義圖表物件
    plt.rcParams['font.sans-serif'] = ['mingliu']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['savefig.dpi'] = 200 #图片像素
    plt.rcParams['figure.dpi'] = 200 #分辨率
  
    ax = plt.subplot(111)
 
    #繪製圖案 ( 圖表 , K線物件 )
    
    
    candlestick_ohlc(ax, KData, width=0.0003, colorup='r', colordown='g')  
    ax.plot_date( Time,FastMA, 'k-' , linewidth=1 ,color='#00FFFF')
    ax.plot_date( Time,SlowMA, 'k-' , linewidth=1 ,color='#FFFF00')
    ax.plot_date( Time,BoxTop, 'k-' , linewidth=1 ,color='#0000FF')
    ax.plot_date( Time,BoxDown, 'k-' , linewidth=1 ,color='#00FF00')

    # X軸的間隔設為半小時
    plt.xticks(np.arange(KData[0][0],KData[-1][0], 1/1440*30))
        
    #定義標頭
    ax.set_title(note)

    #定義x軸
    hfmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(hfmt)
    plt.savefig('C:\\Temp\\'+filename+'.png')#儲存圖片
    plt.close()
   
def drawMap(KBar1M,df,filename,note =None) :
    FastPeriod=10
    SlowPeriod=30 
    KData = KBar1M.GetChartTypeData()
    df = df.sort_values(by=['time'],ascending=True)
    #FastMA=KBar1M.GetMAByOpen(FastPeriod,0)
    #SlowMA=KBar1M.GetMAByOpen(SlowPeriod,0)
    FastMA=pf['ma_s']
    SlowMA=pf['ma_l']
    BoxTop =   df['BoxTop'] 
    BoxDown =df['BoxDown'] 

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
    ax.plot_date( Time,BoxDown, 'k-' , linewidth=1 ,color='#00FF00')
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

def out_excle(name,df,result) :
    writer = pd.ExcelWriter('C:\\temp\\'+ name+'_re.xlsx',engine=None)
    df.to_excel(writer,'0') #將df資料輸出到 '0' 工作表
    result.to_excel(writer,'result') #將result資料輸出到 'result' 工作表
    #將df['cus']資料輸出到'result'工作表，指定第5欄輸出
    #df['cus'].to_excel(writer,'result',startcol=5)
   
    writer.save()

def result_F(df,v,n):
    #計算最後報酬
    last = 0

    if(len(df)>0):
        last = int( df['cus'].iloc[-1])
    #計算交易次數
    count = len(df)
    wamt =int( df['ret'][df['ret']>0].sum())
    lamt =int( df['ret'][df['ret']<0].sum())
    
    #計算最大回檔
    def maxdrawdown(s):
        s = s.cummax() - s #歷史最高價 - 現在序列,cummax 生成當日之前的歷史最高價序列
        return (s.max())
    mdd = 0

    if(len(df)>0):
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
     
    v.append([n[0:6],n,last,wamt,lamt,count,mdd,w])

    return(result)

def out_ResultExcle(filePath,name,allResult) :
    writer = pd.ExcelWriter(filePath + name+'.xlsx',engine=None)
    allResult.to_excel(writer,'result') #將result資料輸出到 'result' 工作表
    writer.save()

def cal_ang(point_1, point_2, point_3):
    """
    根据三点坐标计算夹角
    :param point_1: 点1坐标
    :param point_2: 点2坐标
    :param point_3: 点3坐标
    :return: 返回任意角的夹角值，这里只是返回点2的夹角
    """
    try:
        a=math.sqrt((point_2[0]-point_3[0])*(point_2[0]-point_3[0])+(point_2[1]-point_3[1])*(point_2[1] - point_3[1]))
        b=math.sqrt((point_1[0]-point_3[0])*(point_1[0]-point_3[0])+(point_1[1]-point_3[1])*(point_1[1] - point_3[1]))
        c=math.sqrt((point_1[0]-point_2[0])*(point_1[0]-point_2[0])+(point_1[1]-point_2[1])*(point_1[1]-point_2[1]))
        A=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
        B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
        C=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
    except :
        return 0
    return B

def get_week_of_month(yy,mm,dd):
    begin = int(str(datetime.date(int(yy),int(mm),1).strftime("%W")))
    end = int(str(datetime.date(int(yy),int(mm),int(dd)).strftime("%W")))

    return end - begin + 1

def get_weekday(yy,mm,dd):
    weekday = datetime.date(int(yy),int(mm),int(dd)).isoweekday()
   

    return weekday



FilePath='C:\\temp\\DATA\\'

Broker='MTX'
YYMM ='202103'
FileName ='Daily_2021_03_08.csv'

allColumns =['YYMM','日期','最後報酬','總賺錢點數','總賠錢點數','交易次數','最大回檔','勝率']
allReValues =[]
   

# 找出在資料夾中的日期
filenames=[ day for day in os.listdir(FilePath) if day.find('csv') >=0 ]
filenames.sort()
# 定義要回傳的List




for i in range (len(filenames)):
    #df =   pd.read_csv(FilePath+filenames[i],encoding="UTF8")
    df =   pd.read_csv(FilePath+filenames[i], low_memory=False,encoding="UTF-8",converters={'成交日期':str,'成交時間':str})
    filename =filenames[i]
    yy = filename[6:10]
    mm = filename[11:13]
    dd = filename[14:16]
    YYMM = yy+mm

    if get_week_of_month(yy,mm,dd) == 3 :
        if get_weekday(yy,mm,dd)>3 :
            if(len( str( int(mm)+1))==1):
                YYMM =yy+ str( int(mm)+1).zfill(2)
            else :
                YYMM =yy+ str( int(mm)+1)

    elif get_week_of_month(yy,mm,dd) > 3 :
        if(len( str( int(mm)+1))==1):
            YYMM =yy +  str( int(mm)+1).zfill(2)
        else :
            YYMM =yy + str( int(mm)+1)
  

   

    # print('yy', yy)
    # print('mm',mm)
    # print('dd',dd)
    #print('YYMM',YYMM)
    #print('len(df):',len(df))
    

    data = df[ (df['商品代號'].str.strip() == Broker) &  (df['到期月份(週別)'].str.strip()  == YYMM ) ]# & (df['成交日期']==yy+mm+dd)   ]
    print('len(data):',len(data))
    # 定義K棒物件

    if len(data)==0 :
             continue
    
    Today=datetime.datetime.strptime(data['成交日期'].iloc[0],'%Y%m%d').strftime('%Y%m%d')
   
    KBar1M=KBar(Today,1)  
    # 定義MA週期
    FastPeriod=10
    SlowPeriod=30 
    #starTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 08:45:00','%Y-%m-%d %H:%M:%S')
    #orderTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 09:30:00','%Y-%m-%d %H:%M:%S')
    #endTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 13:30:00','%Y-%m-%d %H:%M:%S')
    
    starTime = time.strptime('15:00:00','%H:%M:%S') #datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 15:00:00','%Y-%m-%d %H:%M:%S')
    orderTime =time.strptime('18:00:00','%H:%M:%S')# datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 18:00:00','%Y-%m-%d %H:%M:%S')
   
    endTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 04:30:00','%Y-%m-%d %H:%M:%S') 
    
    print('starTime',starTime) 
    print('orderTime',orderTime)
    print('starTime',starTime)
    
    columns =['time','close1','close2','close3','Triangle','BC','ret','cus','note']
    reValues =[]
    r=0 #記錄交易資金流量
    b=0 #設定多空方，多方=1，空方=-1，空手=0
    sr = 0 #保險本 
    sb = 0 #保險多空
    L = len(data) #取得筆數
    topProfit = 0 
    boxIndex =0
    order_sign = 0 

    rr = 0 #
    srr = 0

    pf =[]

    msgIndex =0
    for i in  range( len(data)):

        _date =  data['成交日期'].iloc[i]
        _time =  data['成交時間'].iloc[i]
        Price=float(data['成交價格'].iloc[i])
        Qty=float(data['成交數量(B+S)'].iloc[i])
        _t = time.strptime('15:00:00','%H:%M:%S') 
    
    
        if len(_time)==5 :
            _dateTime = _date[0:4]+'-'+_date[4:6]+'-'+_date[6:] +' 0' + _time[0:1]+':' + _time[1:3]+':' + _time[3:]
            _t =  time.strptime('0' + _time[0:1]+':' + _time[1:3]+':' + _time[3:],'%H:%M:%S')
        else :
            _dateTime = _date[0:4]+'-'+_date[4:6]+'-'+_date[6:] +' ' + _time[0:2]+':' + _time[2:4]+':' + _time[4:]
            _t =  time.strptime(_time[0:2]+':' + _time[2:4]+':' + _time[4:],'%H:%M:%S')
        Time=datetime.datetime.strptime(_dateTime,'%Y-%m-%d %H:%M:%S')
        
        

        isok = True

        if _t >= time.strptime('00:00:00','%H:%M:%S') and  _t <= time.strptime('04:30:00','%H:%M:%S') :
            isok= False
        
        if _t >= time.strptime('15:00:00','%H:%M:%S') and  _t <= time.strptime('23:59:59','%H:%M:%S') :
            isok= False
           
        
        if isok :
             continue

        
        
        # 每分鐘判斷一次
        #print('Time',Time,'Price',Price)
        ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
        
        isok = True

        if _t >= orderTime and  _t <= time.strptime('23:59:59','%H:%M:%S') :
            isok= False
        if _t >= time.strptime('00:00:00','%H:%M:%S') and  _t <= time.strptime('04:30:00','%H:%M:%S') :
            
            endTime = datetime.datetime.strptime(Time.strftime('%Y-%m-%d ') +' 04:20:00','%Y-%m-%d %H:%M:%S') 
           
            if Time > endTime :
               
                if b != 0 :
                    r,b,rr,reValues = outp(Time,Price,r,b,note,reValues)
                    topProfit = 0
                    print('Time > endTime Time > endTime Time > endTime Time > endTime Time > endTime Time > endTime ')
                    #drawMap(KBar1M,pf,filename,msg)
            


            isok= False

        if isok :
            continue


        if ChangeKFlag==1:
            #print('Time',Time)
            #print('ChangeKFlag：',ChangeKFlag)
            pf = pd.DataFrame(KBar1M.TAKBar,columns =['time','open','high','low','close','volume'])
            pf = BoxTheory(pf,10,1)
            #print('當前價',Price,'，時間：',Time,'，量：',Qty)
            #print('len(pf1):',len(pf))      
            #pf = BoxTheory(pf,5,0)
            #print('len(pf2):',len(pf))
            pf = pf.sort_values(by=['time'],ascending=False)
            #print(pf)
            #print('--------------------------------------------------------------------------------')
            
           
            
            BoxTop =pf['BoxTop'].iloc[1] 
            BoxDown =pf['BoxDown'].iloc[1] 
            
           
            
            FastMA=KBar1M.GetMAByOpen(FastPeriod,0)
            SlowMA=KBar1M.GetMAByOpen(SlowPeriod,0)

            #print(FastMA)
            #print('--------------------------------------------------------------------------------')
            #print ('close2:',close2,'    close1:',close1,'   Price:',Price)
            #_time =   datetime.datetime.strptime( Time.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M')
#            _ordertime = datetime.datetime.strptime( orderTime.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M')
            
            note =''

            
            

            if len(SlowMA)>=SlowPeriod+2:
                
                
                #Last1FastMA,Last2FastMA=FastMA[-2],FastMA[-1]
                #Last1SlowMA,Last2SlowMA=SlowMA[-2],SlowMA[-1] 
                Last1FastMA,Last2FastMA=pf['ma_s'].iloc[2],pf['ma_s'].iloc[1]
                Last1SlowMA,Last2SlowMA=pf['ma_l'].iloc[2],pf['ma_l'].iloc[1]  

                msg = ''
                msg_b = 0 
                if  Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA:#pf['ma_sign'].iloc[-1] == 1:
                    msg_b = 1
                    msg='黃金交叉 - 做多： Price:'+str(Price) +' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                    msgIndex=0
                    print(msg)
                elif Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA:# pf['ma_sign'].iloc[-1] == -1:
                    msg_b = -1
                    msg='死亡交叉 - 做空： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                    msgIndex=0
                    print(msg)
                elif msgIndex != 1 and   BoxTop < Last2FastMA  and BoxTop < Last2SlowMA :
                    #print('BoxTop',BoxTop ,'Last2FastMA' ,Last2FastMA,'Last2SlowMA',Last2SlowMA)
                    msg_b = 1
                    msg='突破箱頂 - 做多： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                    msgIndex =1
                    print(msg)
                elif  msgIndex != -1 and  BoxDown > Last2FastMA  and BoxDown > Last2SlowMA :   
                    #print('BoxDown',BoxDown ,'Last2FastMA' ,Last2FastMA,'Last2SlowMA',Last2SlowMA) 
                    msg_b = -1
                    msg='突破箱底 - 做空： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                    msgIndex =-1
                    print(msg)

                #if msg_b!= 0 :
                    #saveDrawMap(KBar1M,Time.strftime("%Y%m%d%H%M%S"))
                    #drawMap(KBar1M,pf,Time.strftime("%Y%m%d%H%M%S"),msg)
                    #status_code =  send_message(msg,'C:\\Temp\\'+Time.strftime("%Y%m%d%H%M%S")+'.png')
                    #if(status_code != 200):
                    #    send_message(msg)


                if b != 0 :
    
                    r,b,rr,topProfit,reValues = stopByMA(Time,Price,0.5,-0.5,r,b,topProfit,note,reValues,pf,KBar1M)
                    #if b==0:
                    #    drawMap(KBar1M,pf,filename,msg)
                
                if b == 0 :
                    note=''
                    #if pf['adx'].iloc[1] >25 and Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA :#pf['ma_sign'].iloc[-1] == 1:
                    #    b =1
                    #elif pf['adx'].iloc[1] >25 and Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA :# pf['ma_sign'].iloc[-1] == -1:
                    #    b = -1
                    if pf['adx'].iloc[1] >25 and Price > Last2FastMA and  BoxTop < Last2FastMA  and BoxTop < Last2SlowMA :
                        b = 1
                    elif pf['adx'].iloc[1] >25 and Price < Last2FastMA and BoxDown > Last2FastMA  and BoxDown > Last2SlowMA :   
                        b = -1
 
                    if b!= 0 :
                        r,b,reValues = inp(Time,Price,b,note,reValues)
                        topProfit = r
                        order_sign = 0 
                        #drawMap(KBar1M,pf,filename,msg)
                       

    
   
    reDF = pd.DataFrame(reValues, columns = columns)
    reDF['cus'] = reDF['ret'].cumsum()
    last = 0

    if(len(reDF)>0):
        last = int( reDF['cus'].iloc[-1])
    
    msg = 'filename:'+filename+'last:'+str(last)+' OrderCount:'+str(len(reDF))
    print(msg)
    result = result_F(reDF,allReValues,yy+mm+dd)
    out_excle(filename,reDF,result)
    #out_excle(filename+'_All',pf,pf)
    #drawMap(KBar1M,pf,filename,'')
    #send_message(msg,'C:\\Temp\\'+filename+'.png')






nowTime = int(time.time()) # 取得現在時間
allDf = pd.DataFrame(allReValues, columns = allColumns)
out_ResultExcle(FilePath+'\\OUT\\',str(nowTime),allDf)

            

        
       

 