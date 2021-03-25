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
   
   
    df['BoxTopD'] = df['high'].iloc[:].rolling(N).max()
    df['BoxDownD'] = df['low'].iloc[:].rolling(N).min()
    df['BoxTopN'] = df['high'].iloc[:].shift(1+N).rolling(N).max()
    df['BoxDownN'] = df['low'].iloc[:].shift(1+N).rolling(N).min()
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

        df['BoxTopDef'].iloc[i] = (df['BoxTop'].iloc[i] - df['close'].iloc[i]) * -1
        df['BoxDownDef'].iloc[i] = df['BoxDown'].iloc[i] - df['close'].iloc[i]

        df['BoxTopMax'].iloc[i]  = df['high'].iloc[i-N:i].max()
        df['BoxDownMin'].iloc[i] = df['low'].iloc[i-N:i].min()
        
        # if df['close'].iloc[i-1] > df['close'].iloc[i-2] and df['close'].iloc[i-1] > df['close'].iloc[i] :
        #     df['TriangleTop'].iloc[i-1] = df['close'].iloc[i-1]
        #     df['Triangle'].iloc[i-1]  =   cal_ang((df['close'].iloc[i-2], i-2), (df['close'].iloc[i-1], i-1), (df['close'].iloc[i], i))
        #     df['Triangle_sign'].iloc[i-1] = 1
        # if df['close'].iloc[i-1] < df['close'].iloc[i-2] and df['close'].iloc[i-1] < df['close'].iloc[i] :
        #     df['TriangleDown'].iloc[i-1] = df['close'].iloc[i-1]
        #     df['Triangle'].iloc[i-1]  =   cal_ang((df['close'].iloc[i-2], i-2), (df['close'].iloc[i-1], i-1), (df['close'].iloc[i], i))
        #     df['Triangle_sign'].iloc[i-1] = -1
        
       


        # #設定Box 指標箱型突破高點訊號= 1 (部位買進)df['BoxTop'].iloc[i-1] > df['close'].iloc[i-1] and
        # if ( df['BoxTop'].iloc[i] < df['close'].iloc[i] ) and  df['BoxTopDef'].iloc[i] > S : 
        #     if df['close'].iloc[i] > df['close'].iloc[i-1]:
        #         if topV < df['close'].iloc[i] :
        #             topV = df['close'].iloc[i]
        #             df['box_sign'].iloc[i] = 1
        #             DownV=0
        #             if boxIndexTop == 0 :
        #                 boxIndex = boxIndex + 1 
        #                 boxIndexTop = 1
        #                 boxIndexDown = 0
        #                 boxIndexBL =0
                  
        #             df['BoxIndex'].iloc[i] = boxIndex
           
    
        
        # #設定Box指標箱型突破低點訊號= -1 (部位買進)df['BoxDown'].iloc[i-1] < df['close'].iloc[i-1] and 
        # if (df['BoxDown'].iloc[i] > df['close'].iloc[i] ) and  df['BoxDownDef'].iloc[i] > S  : 
        #     if df['close'].iloc[i] < df['close'].iloc[i-1] :
        #         if DownV ==  0  or  DownV > df['close'].iloc[i] :
        #             DownV = df['close'].iloc[i]
        #             df['box_sign'].iloc[i] = -1
        #             topV=0
        #             if boxIndexDown == 0 :
        #                 boxIndex = boxIndex + 1 
        #                 boxIndexTop = 0
        #                 boxIndexDown = 1  
        #                 boxIndexBL =0               
        #             df['BoxIndex'].iloc[i] = boxIndex
            
        # if (df['BoxTop'].iloc[i] > df['close'].iloc[i] ) &  (df['BoxDown'].iloc[i] < df['close'].iloc[i]): 
        #     if boxIndexBL == 0 :
        #         boxIndexTop = 0
        #         boxIndexDown = 0  
        #         boxIndexBL =1
        #         df['FF'].iloc[i] ='V'            
                             

        # if df['BoxTop'].iloc[i] < df['BoxDown'].iloc[i]  :
        #     df['box_sign'].iloc[i] = 1
        #     df['BoxIndex'].iloc[i] = boxIndex
     
        # if df['BoxDown'].iloc[i] > df['BoxTop'].iloc[i]  :
        #      df['box_sign'].iloc[i] = -1
        #      df['BoxIndex'].iloc[i] = boxIndex

        if (df['close'].iloc[i-1]  >  df['BoxTop'].iloc[i-1] ) and (df['close'].iloc[i]  <  df['BoxTop'].iloc[i] ) :#and (df['Close'].iloc[i]  >  df['BoxDown'].iloc[i] )  :
             df['box_sign'].iloc[i] = -1
        
        if (df['close'].iloc[i-1]  < df['BoxDown'].iloc[i-1] ) and (df['close'].iloc[i]  >  df['BoxDown'].iloc[i] ) :#and (df['Close'].iloc[i]  < df['BoxTop'].iloc[i] )   :
             df['box_sign'].iloc[i] = 1


     


        # if (df['close'].iloc[i-1]  <  df['BoxTop'].iloc[i-1] ) and (df['close'].iloc[i]  >  df['BoxTop'].iloc[i] ) :
        #      df['box_sign'].iloc[i] = 1
        
        # if (df['close'].iloc[i-1]  > df['BoxDown'].iloc[i-1] ) and  (df['close'].iloc[i]  <  df['BoxDown'].iloc[i] ) :
        #      df['box_sign'].iloc[i] = -1 


        if  df['box_sign'].iloc[i] == -1 and  (df['close'].iloc[i]  >  df['BoxDown'].iloc[i] ) :
             df['box_sign'].iloc[i] = 1

        if  df['box_sign'].iloc[i] == 1 and  (df['close'].iloc[i]  <  df['BoxTop'].iloc[i] ) :
             df['box_sign'].iloc[i] = -1



        # df['Triangle'].iloc[i-1]  =   cal_ang((df['Close'].iloc[i-2], i-2), (df['Close'].iloc[i-1], i-1), (df['Close'].iloc[i], i))

        # if (df['Close'].iloc[i-1]  > df['Close'].iloc[i] ) & (df['Close'].iloc[i-1]  >  df['Close'].iloc[i-2] ) :
        #     if df['Triangle'].iloc[i-1]  < 50 and df['Triangle'].iloc[i-1]  > 0:
        #         df['point_sign'].iloc[i-1] = 1 

        # if (df['Close'].iloc[i-1]  < df['Close'].iloc[i] ) & (df['Close'].iloc[i-1]  < df['Close'].iloc[i-2] ) :
        #      if df['Triangle'].iloc[i-1]  < 50 and df['Triangle'].iloc[i-1]  > 0:
        #         df['point_sign'].iloc[i-1] = -1 



    return df     
                   
                    
                
                 
        