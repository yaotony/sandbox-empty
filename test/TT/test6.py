from indicator import getFutureDailyInfo
from indicator import KBar
import pandas as pd
import time ,datetime
import math
import numpy as np
from Order3 import inp,outp,stopByB,stopByS
from Strategy6 import BoxTheory
import os


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
  

   
    print('filename',filename)
    # print('yy', yy)
    # print('mm',mm)
    # print('dd',dd)
    #print('YYMM',YYMM)
    print('len(df):',len(df))
    Today=datetime.datetime.strptime(yy+mm+dd,'%Y%m%d').strftime('%Y%m%d')
   

    data = df[ (df['商品代號'].str.strip() == Broker) &  (df['到期月份(週別)'].str.strip()  == YYMM )  & (df['成交日期']==yy+mm+dd)   ]
    print('len(data):',len(data))
    # 定義K棒物件


    MinuteKbar=KBar(Today,1)    
    starTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 09:00:00','%Y-%m-%d %H:%M:%S')
    orderEndTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 13:00:00','%Y-%m-%d %H:%M:%S')
    orderTime = starTime
    close1=0
    close2=0
    close3=0
    # 定義MA、RSI週期
    MAPeriod=10
    RSIPeriod=30
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

        ChangeKFlag=MinuteKbar.AddPrice(Time,Price,Qty)
        
        # 每分鐘判斷一次
    
    
        note =''
        if ChangeKFlag==1:
            #print('ChangeKFlag：',ChangeKFlag)
            pf = pd.DataFrame(MinuteKbar.TAKBar,columns =['time','open','high','low','close','volume'])
            #print('當前價',Price,'，時間：',Time,'，量：',Qty)
            #print('len(pf1):',len(pf))      
            #pf = BoxTheory(pf,5,0)
            #print('len(pf2):',len(pf))
            pf = pf.sort_values(by=['time'],ascending=False)
            if len(MinuteKbar.GetClose()) < max(MAPeriod,RSIPeriod) :
                continue
            # 取得最新的、上一筆收盤價
            Close=MinuteKbar.GetClose()[-2]
            # 取得最新的、上一筆MA
            FastMA=MinuteKbar.GetWMA(9)[-2]
            SlowMA=MinuteKbar.GetWMA(16)[-2]
            # 取得最新的RSI
            RSI=MinuteKbar.GetRSI(30)[-2]

            High=MinuteKbar.GetHigh()
            # if len(High) >= 15:
            #     # 取前15分鐘的高低點
            #     Ceil=max(High[-15:-1])
            #     Floor=min(MinuteKbar.GetLow()[-15:-1])
            #     # 判斷價格是否突破高低點進場
            #     #print('Ceil',Ceil)
            #     #print('Floor',Floor)
                
            close1 =pf['close'].iloc[1]
            close2 =pf['close'].iloc[2]
            close3 =pf['close'].iloc[3]

            if b == 0 and  Time < orderEndTime :
                # RSI 大於 50 且 價格 > MA 
                    #print('Ceil',Ceil,' Floor',Floor,' Price',Price)
                    Triangle  =   cal_ang((close3, 3), (close2, 2), (close1, 1))

                    if close2 > close3 and close2 > close1 :
                        if Triangle < 50 :
                            orderTime = Time
                            r,b,note,reValues = inp(Time,Price,1,note,reValues)
                            topProfit = r
                            continue
                    elif close2 < close3 and close2 < close1 :
                        if Triangle < 50 :
                            orderTime = Time
                            r,b,note,reValues = inp(Time,Price,-1,note,reValues)
                            topProfit = r
                        
                            continue


        
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
            
            
            if i < L-1 :
                
                if b == 1  or b == -1 :
                    if b == 1 :
                        (r,b,sr,sb,topProfit,rr,srr,note,reValues)=stopByB(Time,Price,0.5,-0.25,r,b,sr,sb,topProfit,note,reValues)
                    elif b==-1 :
                        (r,b,sr,sb,topProfit,rr,srr,note,reValues)=stopByS(Time,Price,0.5,-0.25,r,b,sr,sb,topProfit,note,reValues)
                    
                    # if b==0 :
                    #     reValues.append([Time,close2,close1,Price,Triangle,b,rr,0,note])
                    
                    # if srr != 0:
                    #     reValues.append([Time,close2,close1,Price,Triangle,sb,srr,0,note])
                    #若b=0,表示空手
                if b == 0 :#and ChangeKFlag==1 :
                        a = Price - close1
                        
                        # if ( (a > 0 and  a < 2) or (a < 0 and  a >-2) )and Triangle > 0 and  Triangle < 50  and  _ordertime != _time :
                        #     if close1> close2 and close1 > Price :
                        #         b = 1
                        #     if close1 < close2 and close1 < Price :   
                        #         b = -1

                        #     orderTime = Time
                        #     r,b,note,reValues = inp(Time,Price,b,note,reValues)
                        #     topProfit = r
                        #     #reValues.append([Time,close2,close1,Price,Triangle,b,0,0,note])
                        #     #print('a:', a,' Time',Time, 'close3:',close3,'close2:',close2,'    close1:',close1,'   Price:',Price,' Triangle:',Triangle,'-----及時 ',b)



            elif i == L-1 :
                #若b不等於0 (表示還有部位)
                if b != 0 :
                    r,b,rr,note,reValues = outp(Time,Price,r,b,note,reValues) 
                    #reValues.append([Time,close2,close1,Price,Triangle,b,rr,0,note])
                    topProfit = 0
                    if sb!=0 :                
                        sr,sb,srr,note,reValues = outp(Time,Price,sr,sb,note,reValues)
                        #print('保險出場： sr= ',sr,' sb=',sb,'  srr=',srr )
                        # reValues.append([Time,close2,close1,Price,Triangle,sb,srr,0,note])   
    
    reDF = pd.DataFrame(reValues, columns = columns)
    reDF['cus'] = reDF['ret'].cumsum()
    last = 0

    if(len(reDF)>0):
        last = int( reDF['cus'].iloc[-1])
    
    print(filename,' 最後報酬:',last)
    result = result_F(reDF,allReValues,yy+mm+dd)
    out_excle(filename,reDF,result)






nowTime = int(time.time()) # 取得現在時間
allDf = pd.DataFrame(allReValues, columns = allColumns)
out_ResultExcle(FilePath+'\\OUT\\',str(nowTime),allDf)

            


        
       

 