from LineMSG import linePush
from SendOrderMSG  import sendMSG


# r=0 #記錄交易資金流量
# b=0 #設定多空方，多方=1，空方=-1，空手=0
# topProfit = 0 
# order_sign = 0 下單訊號 1 下一筆下單

def OrderInp(df,r,b,order_sign,topProfit,endTime,boxIndex,result):
    index = len(df)-1 #讀取最後一筆   
    #若b=0,表示空手
    if b == 0 :
        # 是否有下單訊號
        if df['TriangleDown'].iloc[index-1] > 0  or df['TriangleTop'].iloc[index-1] > 0  :  
            if  df['TriangleDown'].iloc[index-1] > 0   :
                b =  1
            elif  df['TriangleTop'].iloc[index-1] > 0   :
                b =  -1
            
            df['sign'].iloc[index] = b #進場時記錄多空
            r = df['Close'].iloc[index] #設定多方買進與空方賣出成本
            df['note'].iloc[index] = df['note'].iloc[index]+ " 進場 - 下單 ： " + str(b) +"  :  " + str(r) 
            linePush( endTime.strftime("%Y-%m-%d %H:%M:%S") +' '+ df['note'].iloc[index])
            topProfit = r 
            order_sign = 0
            result['交易次數'].iloc[0] = result['交易次數'].iloc[0] + 1
            #sendMSG(b,df['Time'].iloc[index],"BoxTheory")
 
    return r,b,order_sign,topProfit,boxIndex,result

def OrderStop(df,wsp,lsp,r,b,topProfit,endTime,result):
    index = len(df)-1 #讀取最後一筆  
 
    try:
       
        TriangleTop = df['TriangleTop'].iloc[index-1]
        TriangleDown = df['TriangleDown'].iloc[index-1]
        #Triangle = df['Triangle'].iloc[index-1]

        if( b == 1  and TriangleTop > 0  ) :
           r,b,result = OrderOut(df,r,b,endTime,result)
           return r,b ,topProfit,result
        
        if( b == -1  and TriangleDown > 0   ) :
            r,b,result = OrderOut(df,r,b,endTime,result)
            return r,b ,topProfit,result
  

    except :
        print('except:'+str(r))

    return r,b ,topProfit,result


def OrderOut(df,r,b,endTime,result):
    index = len(df)-1 #讀取最後一筆 
    #r是資金存量，b=多空方設定 多方=1 空方=-1
    #price=1代表開盤價，price=4代表收盤價
    rr = (df['Close'].iloc[index] - r) * b
    df['ret'].iloc[index] = rr #進場時記錄多空
    df['note1'].iloc[index] = df['note1'].iloc[index] + ' 出場： b=' + str(b) +' ： 下單：' + str(r) +' , 出場：'+ str(df['Close'].iloc[index]) +' ,結算 ： '+str(rr)
    df['note'].iloc[index] = df['note'].iloc[index] +'出場：'+str(int(rr))
    r=0#歸零
    b=0#多空方歸零
    linePush( endTime.strftime("%Y-%m-%d %H:%M:%S") +' '+ df['note1'].iloc[index])
    result['最後報酬'].iloc[0] = result['最後報酬'].iloc[0] + rr
    if rr > 0 :
        result['總賺錢點數'].iloc[0] = result['總賺錢點數'].iloc[0] + rr
    else :
        result['總賠錢點數'].iloc[0] = result['總賠錢點數'].iloc[0] + rr
   
    return r,b,result