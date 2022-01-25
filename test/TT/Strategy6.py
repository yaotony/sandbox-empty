import math
import numpy as np
import talib


def BoxTheory(df,N,S):
    df['BoxTop']  = 0
    df['BoxDown'] = 0
    df['BoxTopN']  = 0
    df['BoxDownN'] = 0
    df['BoxTopD']  = 0
    df['BoxDownD'] = 0
    
   
   
    #Box 交易訊號欄
 
    df['ma_s'] = df['open'].iloc[:].rolling(10).mean()#以收盤價[close]計算5日均線 
    df['ma_l'] = df['open'].iloc[:].rolling(30).mean()#以收盤價[close]計算5日均線 
    df['ma_40'] = df['open'].iloc[:].rolling(40).mean()#以收盤價[close]計算5日均線 
    df['adx'] = talib.ADX(df['high'],df['low'],df['close'],14)
   
   
    df['BoxTopD'] = df['high'].iloc[:].rolling(N).max()
    df['BoxDownD'] = df['low'].iloc[:].rolling(N).min()
    df['BoxTopN'] = df['high'].iloc[:].shift(1+N).rolling(N).max()
    df['BoxDownN'] = df['low'].iloc[:].shift(1+N).rolling(N).min()
  

    topV = 0
    DownV = 0
    boxIndex =0
    BoxIndexOrder=0
    boxIndexTop =0
    boxIndexDown =0
    boxIndexBL = 0
    BoxTop = 0
    BoxDown = 0  

    BoxTopAr =  []
    BoxDownAr = []
    for i in  range( len(df)):
     
        BoxTopD = df['BoxTopD'].iloc[i] 
        BoxTopN = df['BoxTopN'].iloc[i] 
        BoxDownD = df['BoxDownD'].iloc[i] 
        BoxDownN = df['BoxDownN'].iloc[i]
        
        
        if BoxTopD <  BoxTopN :
             BoxTop = BoxTopN
             boxIndexTop = BoxTop
        else :
             BoxTop = boxIndexTop

        if BoxDownD > BoxDownN :
             BoxDown = BoxDownN
             boxIndexDown = BoxDownN
        else :
             BoxDown = boxIndexDown

  
        
        if BoxTop == 0 :
            BoxTop  =  BoxTopD
        if BoxDown == 0 :
            BoxDown  =  BoxDownD
         
        BoxTopAr.append(BoxTop)
        BoxDownAr.append(BoxDown)

    df['BoxTop'] = BoxTopAr
    df['BoxDown'] = BoxDownAr

 
    return df     
                   
                    
                
                 
        