#1313
from Order2 import inp,outp,stop
from StrategyOBV import OBVTheory
from StrategyMA import MA
import math

def cal_ang(point_1, point_2, point_3):
    """
    根据三点坐标计算夹角
    :param point_1: 点1坐标
    :param point_2: 点2坐标
    :param point_3: 点3坐标
    :return: 返回任意角的夹角值，这里只是返回点2的夹角
    """
    a=math.sqrt((point_2[0]-point_3[0])*(point_2[0]-point_3[0])+(point_2[1]-point_3[1])*(point_2[1] - point_3[1]))
    b=math.sqrt((point_1[0]-point_3[0])*(point_1[0]-point_3[0])+(point_1[1]-point_3[1])*(point_1[1] - point_3[1]))
    c=math.sqrt((point_1[0]-point_2[0])*(point_1[0]-point_2[0])+(point_1[1]-point_2[1])*(point_1[1]-point_2[1]))
    A=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
    B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
    C=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
    return B


def BoxTheory(df,N,S):
    #當近期N天內的高點 比 N+1 天前的 N天內高點還低時 ,則 N+1天前的 N天內高點 為近期箱型的頂部。
    #當近期M天內的低點 比 M+1 天前的 M天內低點還高時 ,則 M+1天前的 M天內低點 為近期箱型的底部。
    df['BoxTop']  = 0
    df['BoxDown'] = 0
    df['BoxTopN']  = 0
    df['BoxDownN'] = 0
    df['BoxTopD']  = 0
    df['BoxDownD'] = 0
    df['BoxTopDef']  = 0
    df['BoxDownDef'] = 0
    df['BoxIndex'] = 0
    df['BoxTopMax']  = 0
    df['BoxDownMin'] = 0
    df['TriangleTop'] =0
    df['TriangleDown'] =0
    df['Triangle'] = 0
    df['Triangle_sign'] = 0
    #Box 交易訊號欄
    df['box_sign'] =0
   
   
    df['BoxTopD'] = df['High'].iloc[:].rolling(N).max()
    df['BoxDownD'] = df['Low'].iloc[:].rolling(N).min()
    df['BoxTopN'] = df['High'].iloc[:].shift(1+N).rolling(N).max()
    df['BoxDownN'] = df['Low'].iloc[:].shift(1+N).rolling(N).min()
    df['FF']='' 

    
    topV = 0
    DownV = 0
    boxIndex =0
    boxIndexTop =0
    boxIndexDown =0
    boxIndexBL = 0
    for i in  range( len(df)):
        
        if df['BoxTopD'].iloc[i] <  df['BoxTopN'].iloc[i] :
            df['BoxTop'].iloc[i] =  df['BoxTopN'].iloc[i]
        else :
            df['BoxTop'].iloc[i] =  df['BoxTop'].iloc[i-1]

        if df['BoxDownD'].iloc[i] >  df['BoxDownN'].iloc[i] :
            df['BoxDown'].iloc[i] =  df['BoxDownN'].iloc[i]
        else :
            df['BoxDown'].iloc[i] =  df['BoxDown'].iloc[i-1]
        
        if df['BoxTop'].iloc[i] == 0 :
            df['BoxTop'].iloc[i]  =  df['BoxTopD'].iloc[i]
        if df['BoxDown'].iloc[i] == 0 :
            df['BoxDown'].iloc[i]  =  df['BoxDownD'].iloc[i]

        df['BoxTopDef'].iloc[i] = (df['BoxTop'].iloc[i] - df['Close'].iloc[i]) * -1
        df['BoxDownDef'].iloc[i] = df['BoxDown'].iloc[i] - df['Close'].iloc[i]

        df['BoxTopMax'].iloc[i]  = df['High'].iloc[i-N:i].max()
        df['BoxDownMin'].iloc[i] = df['Low'].iloc[i-N:i].min()
        
        if df['Close'].iloc[i-1] > df['Close'].iloc[i-2] and df['Close'].iloc[i-1] > df['Close'].iloc[i] :
            df['TriangleTop'].iloc[i-1] = df['Close'].iloc[i-1]
            df['Triangle'].iloc[i-1]  =   cal_ang((df['Close'].iloc[i-2], i-2), (df['Close'].iloc[i-1], i-1), (df['Close'].iloc[i], i))
            df['Triangle_sign'].iloc[i-1] = 1
        if df['Close'].iloc[i-1] < df['Close'].iloc[i-2] and df['Close'].iloc[i-1] < df['Close'].iloc[i] :
            df['TriangleDown'].iloc[i-1] = df['Close'].iloc[i-1]
            df['Triangle'].iloc[i-1]  =   cal_ang((df['Close'].iloc[i-2], i-2), (df['Close'].iloc[i-1], i-1), (df['Close'].iloc[i], i))
            df['Triangle_sign'].iloc[i-1] = -1
        
       


        #設定Box 指標箱型突破高點訊號= 1 (部位買進)df['BoxTop'].iloc[i-1] > df['Close'].iloc[i-1] and
        if ( df['BoxTop'].iloc[i] < df['Close'].iloc[i] ) and  df['BoxTopDef'].iloc[i] > S : 
            if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
                if topV < df['Close'].iloc[i] :
                    topV = df['Close'].iloc[i]
                    df['box_sign'].iloc[i] = 1
                    DownV=0
                    if boxIndexTop == 0 :
                        boxIndex = boxIndex + 1 
                        boxIndexTop = 1
                        boxIndexDown = 0
                        boxIndexBL =0
                  
                    df['BoxIndex'].iloc[i] = boxIndex
           
    
        
        #設定Box指標箱型突破低點訊號= -1 (部位買進)df['BoxDown'].iloc[i-1] < df['Close'].iloc[i-1] and 
        if (df['BoxDown'].iloc[i] > df['Close'].iloc[i] ) and  df['BoxDownDef'].iloc[i] > S  : 
            if df['Close'].iloc[i] < df['Close'].iloc[i-1] :
                if DownV ==  0  or  DownV > df['Close'].iloc[i] :
                    DownV = df['Close'].iloc[i]
                    df['box_sign'].iloc[i] = -1
                    topV=0
                    if boxIndexDown == 0 :
                        boxIndex = boxIndex + 1 
                        boxIndexTop = 0
                        boxIndexDown = 1  
                        boxIndexBL =0               
                    df['BoxIndex'].iloc[i] = boxIndex
            
        if (df['BoxTop'].iloc[i] > df['Close'].iloc[i] ) &  (df['BoxDown'].iloc[i] < df['Close'].iloc[i]): 
            if boxIndexBL == 0 :
                boxIndexTop = 0
                boxIndexDown = 0  
                boxIndexBL =1
                df['FF'].iloc[i] ='V'            
                             

        if df['BoxTop'].iloc[i] < df['BoxDown'].iloc[i]  :
            df['box_sign'].iloc[i] = 1
            df['BoxIndex'].iloc[i] = boxIndex
     
        if df['BoxDown'].iloc[i] > df['BoxTop'].iloc[i]  :
             df['box_sign'].iloc[i] = -1
             df['BoxIndex'].iloc[i] = boxIndex


    #進行買賣
    K = 5  #設定保留K線參數
    L = len(df) #取得筆數
    r=0 #記錄交易資金流量
    b=0 #設定多空方，多方=1，空方=-1，空手=0
    df['sign']=0 #新增欄位，用來記錄進場多空
    df['ret']=0 #新增欄位，用來記錄出勤結算
    df['note']='' #記錄交易指數
    df['note1']='' #記錄交易指數
    df['AA']='' 
    df['BB']='' 
    df['CC']='' 
    df['DD']='' 
    df['EE']='' 
  

    #由於序號從0開始，迴圈從第k-1筆記錄開始執行
  
    topProfit = 0 
    boxIndex =0
    order_sign = 0 
    for i in range(K-1,L):
    
        #若 i < 最後一筆，則執行
        if i < L-1 :
            #若 b = 1 ,表示多
            if b == 1  or b == -1 :
                (r,b,topProfit)=stop(df,0.5,-0.1,r,b,i,topProfit)
                
                     
        
            
                #若b=0,表示空手
            if b == 0 :
                if order_sign == 0 :
                    if  df['Triangle_sign'].iloc[i] == 1  and   df['Triangle'].iloc[i-1] < 30 :
                        order_sign = 1 
                        continue
                    elif  df['Triangle_sign'].iloc[i] == -1  and   df['Triangle'].iloc[i-1] < 30 :
                        order_sign = -1 
                        continue
                


                if order_sign == 1   :
                    r,b = inp(df,r,1,i+1)
                    topProfit = r
                    order_sign = 0 

                elif order_sign == -1  : 
                    r,b = inp(df,r,-1,i+1)
                    topProfit = r
                    order_sign = 0 
                else :
                    order_sign = 0 
                
        elif i == L-1 :
            #若b不等於0 (表示還有部位)
            print('最後一筆')
            if b != 0 :
                (r,b) = outp(df,r,b,4,i)
                topProfit = 0
                   
                   
                    
                
                 
        