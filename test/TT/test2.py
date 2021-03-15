from indicator import getFutureDailyInfo
from indicator import KBar
import pandas as pd
import time ,datetime
import math
import numpy as np
from Order3 import inp,outp,stopByB,stopByS
from Strategy6 import BoxTheory

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



FilePath='C:\\temp\\DATA\\'

Broker='MTX'
YYMM ='202001'
FileName ='Daily_2020_01_14.csv'
dd ='2020-01-14'
ddd ='20200114'

df =   pd.read_csv(FilePath+FileName, low_memory=False,encoding="UTF-8",converters={'成交日期':str,'成交時間':str})
print('len(df):',len(df))
Today=datetime.datetime.strptime(ddd,'%Y%m%d').strftime('%Y%m%d')



data = df[ (df['商品代號']==Broker) & (df['到期月份(週別)']==YYMM) & (df['成交日期']==ddd)   ]
#print('data len = ',len(df))
#(df['商品代號']=='MTX') & (df['到期月份(週別)']=='202103') & (df['成交日期']=='20210305')
# 定義K棒物件

KBar1M=KBar(Today,1)    
starTime = datetime.datetime.strptime(dd+' 09:00:00','%Y-%m-%d %H:%M:%S')
orderTime = starTime
close1=0
close2=0
close3=0

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

rr = 0
srr = 0
print('len(data):',len(data))

for i in  range( len(data)):

    _date =  data['成交日期'].iloc[i]
    _time =  data['成交時間'].iloc[i]
    Price=float(data['成交價格'].iloc[i])
    Qty=float(data['成交數量(B+S)'].iloc[i])
   
  
    if len(_time)==5 :
        _dateTime = _date[0:4]+'-'+_date[4:6]+'-'+_date[6:] +' 0' + _time[0:1]+':' + _time[1:3]+':' + _time[3:]
    else :
        _dateTime = _date[0:4]+'-'+_date[4:6]+'-'+_date[6:] +' ' + _time[0:2]+':' + _time[2:4]+':' + _time[4:]
    
    Time=datetime.datetime.strptime(_dateTime,'%Y-%m-%d %H:%M:%S')
     
    if Time < starTime :
        continue

    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    
    # 每分鐘判斷一次
   
   

    if ChangeKFlag==1:
        #print('ChangeKFlag：',ChangeKFlag)
        pf = pd.DataFrame(KBar1M.TAKBar,columns =['time','open','high','low','close','volume'])
        #print('當前價',Price,'，時間：',Time,'，量：',Qty)
        #print('len(pf1):',len(pf))      
        #pf = BoxTheory(pf,5,0)
        #print('len(pf2):',len(pf))
        pf = pf.sort_values(by=['time'],ascending=False)
 

       
        Triangle = 0
        if len(pf)>=4:

            close1 =pf['close'].iloc[1]
            close2 =pf['close'].iloc[2]
            close3 =pf['close'].iloc[3]

            #print('Time',Time, ' close3:',close3,' close2:',close2,'    close1:',close1)
        
            # if close2 > close3 and close2 > close1 :
            #     Triangle  =   cal_ang((close3, 3), (close2, 2), (close1, 1))
            #     if Triangle < 50 :
            #         print('Time',Time, ' close3:',close3,' close2:',close2,'    close1:',close1,' Triangle:',Triangle,' 1')
            # if close2 < close3 and close2 < close1 :
            #     Triangle  =   cal_ang((close3, 3), (close2, 2), (close1, 1))
            #     if Triangle < 50 :
            #         print('Time',Time,' close3:',close3,' close2:',close2,'    close1:',close1,' Triangle:',Triangle,' -1')




    if close1 >0 and close2 >0  :
    
        #print ('close2:',close2,'    close1:',close1,'   Price:',Price)
        _time =   datetime.datetime.strptime( Time.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M')
        _ordertime = datetime.datetime.strptime( orderTime.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M')
        
        Triangle  =   cal_ang((Price, 1), (close1, 2), (close2, 3))
        
        note =''
        if i < L-1 :
            
            if b == 1  or b == -1 :
                if b == 1 :
                    (r,b,sr,sb,topProfit,rr,srr,note)=stopByB(Price,0.5,-0.25,r,b,sr,sb,topProfit,note,Time)
                elif b==-1 :
                    (r,b,sr,sb,topProfit,rr,srr,note)=stopByS(Price,0.5,-0.25,r,b,sr,sb,topProfit,note,Time)
                
                if b==0 :
                    reValues.append([Time,close2,close1,Price,Triangle,b,rr,0,note])
                
                if srr != 0:
                    reValues.append([Time,close2,close1,Price,Triangle,sb,srr,0,note])
                 #若b=0,表示空手
            if b == 0 :#and ChangeKFlag==1 :
                    a = Price - close1
                    
                    if ( (a > 0 and  a < 2) or (a < 0 and  a >-2) )and Triangle > 0 and  Triangle < 50  and  _ordertime != _time :
                        if close1> close2 and close1 > Price :
                            b = 1
                        if close1 < close2 and close1 < Price :   
                            b = -1

                        orderTime = Time
                        r,b,note = inp(Price,b,note)
                        topProfit = r
                        reValues.append([Time,close2,close1,Price,Triangle,b,0,0,note])
                        print('a:', a,' Time',Time, 'close3:',close3,'close2:',close2,'    close1:',close1,'   Price:',Price,' Triangle:',Triangle,'-----及時 ',b)



        elif i == L-1 :

            #若b不等於0 (表示還有部位)
            if b != 0 :
                r,b,rr,note = outp(Price,r,b,note) 
                reValues.append([Time,close2,close1,Price,Triangle,b,rr,0,note])
                topProfit = 0
                if sb!=0 :                
                    sr,sb,srr,note = outp(Price,sr,sb,note)
                    print('保險出場： sr= ',sr,' sb=',sb,'  srr=',srr )
                    reValues.append([Time,close2,close1,Price,Triangle,sb,srr,0,note])   

nowTime = int(time.time()) # 取得現在時間

reDF = pd.DataFrame(reValues, columns = columns)
#print(reDF)
print('cus=',str(reDF['ret'].cumsum()))
out_ResultExcle(FilePath,str(nowTime),reDF)

#df['ma_s'] = df.iloc[:,4].rolling(s).mean()#以收盤價[close]計算5日均線 

            


        
       

 