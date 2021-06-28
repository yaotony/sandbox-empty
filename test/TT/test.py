from indicator import getFutureDailyInfo
from indicator import KBar
import pandas as pd
import time ,datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
from LineMSG import send_message,send_bs_message,send_All_message
import math
import numpy as np
from Order2 import inp,outp,stop,stopByMA
from Strategy6 import BoxTheory
import os
import haohaninfo
from order import Record
from Log import add
from FunOrder import efOrder,getPositionQty

def get_week_of_month(yy,mm,dd):
    begin = int(str(datetime.date(int(yy),int(mm),1).strftime("%W")))
    end = int(str(datetime.date(int(yy),int(mm),int(dd)).strftime("%W")))

    return end - begin + 1

def get_weekday(yy,mm,dd):
    weekday = datetime.date(int(yy),int(mm),int(dd)).isoweekday()
   

    return weekday

def out_excle(name,df,result) :
    writer = pd.ExcelWriter('E:\\temp\\'+ name+'_re.xlsx',engine=None)
    df.to_excel(writer,'0') #將df資料輸出到 '0' 工作表
    result.to_excel(writer,'result') #將result資料輸出到 'result' 工作表
    #將df['cus']資料輸出到'result'工作表，指定第5欄輸出
    #df['cus'].to_excel(writer,'result',startcol=5)
   
    writer.save()

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
    ax.plot_date( Time,FastMA,'-b' ,  linewidth=1 )
    ax.plot_date( Time,SlowMA,'-g' , linewidth=1)
    ax.plot_date( Time,BoxTop,'-y' , linewidth=1)
    ax.plot_date( Time,BoxDown,'-c', linewidth=1)

    # X軸的間隔設為半小時
    plt.xticks(np.arange(KData[0][0],KData[-1][0], 1/1440*30))
        
    #定義標頭
    ax.set_title(note)

    #定義x軸
    hfmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(hfmt)
    plt.savefig('E:\\Temp\\'+filename+'.png')#儲存圖片
    plt.close()

def loadData(KBar1M ,Product,starTime):
    # 定義交易商品
    #Product='MXFD1'
    Today=datetime.datetime.now().strftime('%Y%m%d')
    # 定義券商  、Simulator 虛擬期權
    
    FilePath='E:\\DATA\\simulator\\'+Today+'\\'+Product+'_Match.TXT'

    df =   pd.read_csv(FilePath, low_memory=False,encoding="UTF-8",header=None)
    for i in  range( len(df)):
        Time=datetime.datetime.strptime(df.iloc[i,0],'%Y/%m/%d %H:%M:%S.%f')
        Price=float(df.iloc[i,2])
        Qty=float(df.iloc[i,3])

        if Time < starTime  :
            continue
        
        ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    
    print('歷史資料筆數：',len(df))

def run(Product , starTime,endTime,orderTime) :

    # 定義交易商品
   
    # 定義券商  、Simulator 虛擬期權
    Broker='Simulator'


    # 定義K棒物件
    Today=datetime.datetime.now().strftime('%Y%m%d')
    mmlist=['','A','B','C','D','E','F','G','H','I','J','K','L']

    yy = Today[0:4]
    mm = Today[4:6]
    dd = Today[6:8]
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

    print('YYMM',YYMM)
    Product=f'MXF{mmlist[int(YYMM[5:6])]}{YYMM[3:4]}'
    print('Product',Product)
    KBar1M=KBar(Today,1)
    
    # 定義初始倉位
    OrderRecord=Record()

    # 訂閱報價
    GO = haohaninfo.GOrder.GOQuote()

    columns =['time','close1','close2','close3','Triangle','BC','ret','cus','note']
    reValues =[]
    r=0 #記錄交易資金流量
    b=0 #設定多空方，多方=1，空方=-1，空手=0
    topProfit = 0 
    FastPeriod=10
    SlowPeriod=30
    note='' 
    print('Today',Today)
    print('YYMM',YYMM)
    print('starTime ',starTime)
    print('orderTime ',orderTime)
    print('endTime ',endTime)
    loadData(KBar1M,Product,starTime)

    for row in GO.Subscribe( Broker, 'match', Product ):
       
        # 取得時間、價格欄位
        Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
        Price=float(row[2])
        Qty=float(row[3])
        
        # 將資料填入K棒


        if Time < starTime :
                continue


        ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
        if ChangeKFlag==1:
            print('當前價',Price,'，時間：',Time,'，量：',Qty)
            

        # 每分鐘判斷一次
    
        if Time < orderTime :
                continue

        if Time > endTime :
            GO.EndSubscribe()
            
            OpenInterest = OrderRecord.GetOpenInterest()
            if  OpenInterest != 0 :
                BSN = 0
                BS =''
                if(OpenInterest > 0 ) : 
                    BSN = 1
                    BS ='S'
                elif (OpenInterest < 0 ) :
                    BSN = -1       
                    BS ='B'
                #if datetime.datetime.now().hour >=9 and datetime.datetime.now().hour < 14 and getPositionQty()  > 0:
                #    Price = efOrder(YYMM,BS,1)
                OrderRecord.Cover(BS,Product,Time,Price,1)
                send_bs_message(f'{Time} 出場：{BS} 價格：{Price} 口數：1 結果：{ (Price - r) * BSN}')
                add(starTime.strftime('%Y%m%d%H%M%S'),[Time,'out',Product,BS,Price,1,0])
            
            if b != 0 :
                r,b,rr,reValues = outp(Time,Price,r,b,note,reValues)
                topProfit = 0
                add(starTime.strftime('%Y%m%d%H%M%S'),[Time,'out','MTXS',b,Price,1,rr])
            continue
        if ChangeKFlag==1:
           
            pf = pd.DataFrame(KBar1M.TAKBar,columns =['time','open','high','low','close','volume'])
            #print('當前價',Price,'，時間：',Time,'，量：',Qty)
            pf =    BoxTheory(pf,10,1)       
            pf =pf.sort_values(by=['time'],ascending=False)

            if(len(pf) < 2)  :
                continue

            BoxTop = pf['BoxTop'].iloc[1] 
            BoxDown =pf['BoxDown'].iloc[1] 

                
            FastMA=KBar1M.GetMAByOpen(FastPeriod,0)
            SlowMA=KBar1M.GetMAByOpen(SlowPeriod,0)

      


            if len(SlowMA)>=SlowPeriod+2:
                                
                Last1FastMA,Last2FastMA=pf['ma_s'].iloc[2],pf['ma_s'].iloc[1]
                Last1SlowMA,Last2SlowMA=pf['ma_l'].iloc[2],pf['ma_l'].iloc[1]  


                msg = ''
                msg_b = 0 
                if  Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA:#pf['ma_sign'].iloc[-1] == 1:
                    msg_b = 1
                    msg='黃金交叉 - 做多： Price:'+str(Price) +' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                elif Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA:# pf['ma_sign'].iloc[-1] == -1:
                    msg_b = -1
                    msg='死亡交叉 - 做空： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                elif   BoxTop < Last2FastMA  and BoxTop < Last2SlowMA :
                    #print('BoxTop',BoxTop ,'Last2FastMA' ,Last2FastMA,'Last2SlowMA',Last2SlowMA)
                    msg_b = 1
                    msg='突破箱頂 - 做多： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                elif    BoxDown > Last2FastMA  and BoxDown > Last2SlowMA :   
                    #print('BoxDown',BoxDown ,'Last2FastMA' ,Last2FastMA,'Last2SlowMA',Last2SlowMA) 
                    msg_b = -1
                    msg='突破箱底 - 做空： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
               


                if msg_b!= 0 :
                    saveDrawMap(KBar1M,pf,Time.strftime("%Y%m%d%H%M%S"),msg)
                    status_code =  send_message(msg,'E:\\Temp\\'+Time.strftime("%Y%m%d%H%M%S")+'.png')

                    if(status_code != 200):
                        send_message(msg)

                if Price > BoxTop :
                    msg='價格突破箱頂 - 做多： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                elif Price < BoxDown :
                    msg='價格突破箱底 - 做空： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")

                if msg_b== 0 :
                    msg='Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                    saveDrawMap(KBar1M,pf,Time.strftime("%Y%m%d%H%M%S"),msg)
                
                status_code =  send_All_message(msg,'E:\\Temp\\'+Time.strftime("%Y%m%d%H%M%S")+'.png')
                if(status_code != 200):
                    print(f'status_code:{status_code}')
                    send_All_message(msg)



                OpenInterest = OrderRecord.GetOpenInterest()
                BS=''

                if  OpenInterest != 0 :
                    BSN = 0
                    if(OpenInterest > 0 ) : 
                        BSN = 1
                    elif (OpenInterest < 0 ) :
                        BSN = -1
  

                    if(OpenInterest == 1 and orderTopProFit < Price) : 
                        orderTopProFit = Price
                    elif (OpenInterest == -1 and orderTopProFit > Price) :
                        orderTopProFit = Price
                    
                    if  Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA and (((topProfit - r ) * BSN ) * 0.5) < (topProfit - Price ) * BSN :
                        BS ='B'
                    elif Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA and (((topProfit - r ) * BSN ) * 0.5) < (topProfit - Price ) * BSN :
                        BS ='S'    

                    #if  BSN== 1 and Price < Last2FastMA and  (Price - r) * BSN < -40 :
                    #    BS ='S'
                    #elif  BSN== -1 and Price > Last2FastMA and (Price - r) * BSN < -40:
                    #    BS ='B'                
                
                    if (BS == 'B' and BSN == -1 ) or (BS == 'S' and BSN == 1 ):
                        #if datetime.datetime.now().hour >=9 and datetime.datetime.now().hour < 14 and getPositionQty()  > 0 :
                        #    Price = efOrder(YYMM,BS,1)
                        #    print(f'Price:{Price}')
                        OrderRecord.Cover(BS,Product,Time,Price,1)
                        send_bs_message(f'{Time} 出場：{BS} 價格：{Price} 口數：1 結果：{ (Price - r) * BSN}')
                        add(starTime.strftime('%Y%m%d%H%M%S'),[Time,'out',Product,BS,Price,1,0]) 


                if b != 0 :
    
                    r,b,rr,topProfit,reValues = stopByMA(Time,Price,0.5,-0.5,r,b,topProfit,note,reValues,pf,KBar1M)
                    if b==0:
                        add(starTime.strftime('%Y%m%d%H%M%S'),[Time,'out','MTXS',b,Price,1,rr])


                OpenInterest = OrderRecord.GetOpenInterest()
                
                if OpenInterest == 0 or b == 0 :

                    reDF = pd.DataFrame(reValues, columns = columns)
                    cus  = 0 
                    last = 0
                    lamt = 0

                    BS=''
                    b=0
                    
                    orderCount = len(reDF)#計算交易次數
                    last = int( reDF['ret'].sum())
                    lamt =int( reDF['ret'][reDF['ret']<0].sum())
                    wamt =int( reDF['ret'][reDF['ret']>0].sum())
                   
                    if   Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA :#pf['ma_sign'].iloc[-1] == 1:
                        BS ='B'
                    elif  Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA :# pf['ma_sign'].iloc[-1] == -1:
                        BS ='S'
                    
                    #if BS != '' and   last < -100  :
                        #BS =''
                        #send_bs_message(f'{Time} 強制停止下單！損益：{last} 下單：{BS} 價格：{Price} 口數：1 ')


                    if BS != '' :
                        #if datetime.datetime.now().hour >=9 and datetime.datetime.now().hour < 14 and getPositionQty()  == 0:
                        #    Price = efOrder(YYMM,BS,1)
                        orderTopProFit = 0
                        OrderRecord.Order(BS,Product,Time,Price,1)
                        orderTopProFit = Price
                        
                        send_bs_message(f'{Time} 下單：{BS} 價格：{Price} 口數：1 ')
                        add(starTime.strftime('%Y%m%d%H%M%S'),[Time,'in',Product,BS,Price,1,0])                    


                    if   Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA :#pf['ma_sign'].iloc[-1] == 1:
                        b =1
                    elif  Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA :# pf['ma_sign'].iloc[-1] == -1:
                        b = -1
                    
                    #if b!= 0  and (  last < -100  )  :
                    #    b =0
 
                    if b!= 0 :
                        r,b,reValues = inp(Time,Price,b,note,reValues)
                        add(starTime.strftime('%Y%m%d%H%M%S'),[Time,'in','MTXS',b,Price,1,0])
                        topProfit = r
                    else :
                        b = 0

                    
    
while True :

    Product='MXFE1'
    starTime = datetime.datetime.now()
    orderTime = datetime.datetime.now()
    endTime = datetime.datetime.now()
    overTime = datetime.datetime.now()

    if datetime.datetime.now().hour >6 and datetime.datetime.now().hour < 14 :
        starTime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d')+' 08:40:00','%Y-%m-%d %H:%M:%S')
        orderTime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d')+' 09:15:00','%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d') +' 13:30:00','%Y-%m-%d %H:%M:%S')
        overTime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d') +' 13:32:00','%Y-%m-%d %H:%M:%S')
    else :

        starTime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d')+' 15:00:00','%Y-%m-%d %H:%M:%S')
        orderTime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d')+' 15:30:00','%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.now() + datetime.timedelta(days=1)
        endTime = datetime.datetime.strptime(end_date.strftime('%Y-%m-%d') +' 04:30:00','%Y-%m-%d %H:%M:%S')
        overTime = datetime.datetime.strptime(end_date.strftime('%Y-%m-%d') +' 04:32:00','%Y-%m-%d %H:%M:%S')

    if datetime.datetime.now() > starTime  and datetime.datetime.now() < overTime :
        run(Product,starTime,endTime,orderTime)
    else :
        time.sleep(60)
        print('不在下單時間內容~',datetime.datetime.now())


  
       
