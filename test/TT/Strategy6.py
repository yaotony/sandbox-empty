import math


def BoxTheory(df,N,S):
    df['BoxTop']  = 0
    df['BoxDown'] = 0
    df['BoxTopN']  = 0
    df['BoxDownN'] = 0
    df['BoxTopD']  = 0
    df['BoxDownD'] = 0
    df['BoxTopDef']  = 0
    df['BoxDownDef'] = 0
    df['BoxIndex'] = 0
    df['BoxIndexOrder'] = 0
    df['BoxTopMax']  = 0
    df['BoxDownMin'] = 0
   
   
    #Box 交易訊號欄
    df['box_sign'] =0
   
    s = 10
    l = 30
   
    df['BoxTopD'] = df['high'].iloc[:].rolling(N).max()
    df['BoxDownD'] = df['low'].iloc[:].rolling(N).min()
    df['BoxTopN'] = df['high'].iloc[:].shift(1+N).rolling(N).max()
    df['BoxDownN'] = df['low'].iloc[:].shift(1+N).rolling(N).min()
    df['FF']='' 
      #平均線產生
    df['ma_s'] = df['open'].iloc[:].rolling(s).mean()#以收盤價[close]計算5日均線 
    df['ma_l'] = df['open'].iloc[:].rolling(l).mean()#以收盤價[close]計算5日均線 
    df['ma_5'] = df['open'].iloc[:].rolling(5).mean()#以收盤價[close]計算5日均線 
    #MA 交易訊號欄
    df['ma_sign']=0
    df['ma_index']=0
    #設定黃金交叉訊號
    #df['ma_sign'][(df['ma_s'].shift(1) < df['ma_l'].shift(1)) & (df['ma_s'] > df['ma_l']) ]=1
    #設定死亡交叉訊號
    #df['ma_sign'][(df['ma_s'].shift(1) > df['ma_l'].shift(1)) & (df['ma_s'] < df['ma_l']) ]=-1
  
    ma_index =0

    #OBVTheory(df,5,10) 
    #MA(10,30,df)
    #RSI(5,df)

    topV = 0
    DownV = 0
    boxIndex =0
    BoxIndexOrder=0
    boxIndexTop =0
    boxIndexDown =0
    boxIndexBL = 0
    for i in  range( len(df)-1):
      
       
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

    #     df['BoxTopDef'].iloc[i] = (df['BoxTop'].iloc[i] - df['close'].iloc[i]) * -1
    #     df['BoxDownDef'].iloc[i] = df['BoxDown'].iloc[i] - df['close'].iloc[i]

    #     df['BoxTopMax'].iloc[i]  = df['high'].iloc[i-5:i].max()
    #     df['BoxDownMin'].iloc[i] = df['low'].iloc[i-5:i].min()  
    #     #df['BoxTopMax'].iloc[i]  = df['High'].iloc[i-60:i].max()
        #df['BoxDownMin'].iloc[i] = df['Low'].iloc[i-60:i].min()

        
        # #設定Box 指標箱型突破高點訊號= 1 (部位買進)df['BoxTop'].iloc[i-1] > df['close'].iloc[i-1] and
        # if ( df['BoxTop'].iloc[i] < df['close'].iloc[i] )  : 
        #     boxIndexOrder = boxIndexOrder + 1
        #     df['BoxIndexOrder'].iloc[i] = boxIndexOrder     
        #     if df['close'].iloc[i] > df['BoxTopMax'].iloc[i] and df['close'].iloc[i-1] < df['close'].iloc[i] :#and   boxIndexOrder <= 10 :
        #         if topV < df['close'].iloc[i] :#and df['Volume'].iloc[i] > 1000:
        #             topV = df['close'].iloc[i]
        #             df['box_sign'].iloc[i] = 1
        #             #DownV=0
        #             if boxIndexTop == 0 :
        #                 boxIndex = boxIndex + 1 
        #                 boxIndexTop = 1
        #                 boxIndexDown = 0
        #                 boxIndexBL =0
                  
        #             df['BoxIndex'].iloc[i] = boxIndex
            
            
        
        

                    
                    
           
    
        
        # #設定Box指標箱型突破低點訊號= -1 (部位買進)df['BoxDown'].iloc[i-1] < df['close'].iloc[i-1] and 
        # elif (df['BoxDown'].iloc[i] > df['close'].iloc[i] ) : 
        #     boxIndexOrder = boxIndexOrder + 1
        #     df['BoxIndexOrder'].iloc[i] = boxIndexOrder  
        #     if  df['close'].iloc[i] < df['BoxDownMin'].iloc[i] and df['close'].iloc[i-1] > df['close'].iloc[i] :#and   boxIndexOrder <= 10:#
        #         if DownV ==  0  or  DownV > df['close'].iloc[i]  :#and df['Volume'].iloc[i] > 1000:
        #             DownV = df['close'].iloc[i]
        #             df['box_sign'].iloc[i] = -1
        #             #topV=0
        #             if boxIndexDown == 0 :
        #                 boxIndex = boxIndex + 1 
        #                 boxIndexTop = 0
        #                 boxIndexDown = 1  
        #                 boxIndexBL =0               
        #             df['BoxIndex'].iloc[i] = boxIndex
               
        
        # else :
        #     boxIndexOrder = 0

            
        # if (df['BoxTop'].iloc[i] > df['close'].iloc[i] ) &  (df['BoxDown'].iloc[i] < df['close'].iloc[i]): 
        #      if boxIndexBL == 0 :
        #          boxIndexTop = 0
        #          boxIndexDown = 0  
        #          boxIndexBL =1
        #          df['FF'].iloc[i] ='V'            
                             

        # if df['BoxTop'].iloc[i] < df['BoxDown'].iloc[i]  :
        #     df['box_sign'].iloc[i] = 1
        #     df['BoxIndex'].iloc[i] = boxIndex
     
        # if df['BoxDown'].iloc[i] > df['BoxTop'].iloc[i]  :
        #      df['box_sign'].iloc[i] = -1
        #      df['BoxIndex'].iloc[i] = boxIndex


    return df     
                   
                    
                
                 
        