from LineMSG import linePush
from SendOrderMSG  import sendMSG


# r=0 #記錄交易資金流量
# b=0 #設定多空方，多方=1，空方=-1，空手=0
# topProfit = 0 
# order_sign = 0 下單訊號 1 下一筆下單

def OrderInp(df,r,b,order_sign,topProfit,endTime,boxIndex,result):
    index = len(df)-1 #讀取最後一筆   
    isOk =False
   
    #若b=0,表示空手
    if b == 0 :
        # 是否有下單訊號
        if order_sign == 0 :
            if  df['box_sign'].iloc[index] == 1  :
                order_sign = 1
            elif  df['box_sign'].iloc[index] == -1   :
                order_sign = -1      
        else :       
            if order_sign == 1 or order_sign == -1 :   
                
                #if(  df['box_sign'].iloc[index] == 1 and  order_sign == 1 and  df['Close'].iloc[index] > df['Close'].iloc[index-1] and df['Close'].iloc[index] > df['BoxTop'].iloc[index-1]) :
                if( df['box_sign'].iloc[index] == 1 and  order_sign == 1  and  df['Close'].iloc[index] > df['BoxTopMax'].iloc[index] ):
                    isOk = True
                #elif( df['box_sign'].iloc[index] == -1 and order_sign == -1 and  df['Close'].iloc[index] < df['Close'].iloc[index-1] and df['Close'].iloc[index] < df['BoxDown'].iloc[index-1]) :
                elif( df['box_sign'].iloc[index] == -1 and order_sign == -1  and df['Close'].iloc[index] < df['BoxDownMin'].iloc[index] ):
                    isOk = True
                else :
                    isOk =False
                    order_sign = 0
                    b = 0
                
                
                
                if isOk == True :
                    if  df['BoxIndex'].iloc[index] != boxIndex :
                        b =  order_sign
                        df['sign'].iloc[index] = b #進場時記錄多空
                        r = df['Close'].iloc[index] #設定多方買進與空方賣出成本
                        df['note'].iloc[index] = df['note'].iloc[index]+ " 進場 - 下單 ： " + str(b) +"  :  " + str(r) 
                        linePush( str(df['BoxIndex'].iloc[index]) +' : '+endTime.strftime("%Y-%m-%d %H:%M:%S") +' '+ df['note'].iloc[index])
                        topProfit = r 
                        order_sign = 0
                        boxIndex = df['BoxIndex'].iloc[index]
                        result['交易次數'].iloc[0] = result['交易次數'].iloc[0] + 1
                        #sendMSG(b,df['Time'].iloc[index],"BoxTheory")
            

    return r,b,order_sign,topProfit,boxIndex,result

def OrderStop(df,wsp,lsp,r,b,topProfit,endTime,result):
    index = len(df)-1 #讀取最後一筆  
    mp = 0

    mm = df['Close'].iloc[index] 
    mp = ( (int(mm) - int(r)) / int(r) )  * 100 * b
    if(b == 1 and topProfit < mm) : 
        topProfit = mm
    elif (b == -1 and topProfit > mm) :
        topProfit = mm
        
    df['AA'].iloc[index] = ((topProfit - r ) * b )
    df['BB'].iloc[index] = ((topProfit - r ) * b ) * wsp
    df['CC'].iloc[index] = ((topProfit - mm) * b )
    df['DD'].iloc[index] = mp
    print("df['AA'].iloc[index]:"+str(df['AA'].iloc[index]))
    print("df['BB'].iloc[index]:"+str(df['BB'].iloc[index]))
    print("df['CC'].iloc[index]:"+str(df['CC'].iloc[index]))
    print("df['DD'].iloc[index]:"+str(df['DD'].iloc[index]))
        #
    if ((topProfit - r ) * b ) > 0 :
        if (((topProfit - r ) * b ) * wsp) < (topProfit - mm ) * b  :
            #print('苻合停利+')
            #linePush(endTime.strftime("%Y-%m-%d %H:%M:%S") +' '+'苻合停利+出場')
            r,b,result = OrderOut(df,r,b,endTime,result) 
            return r,b ,topProfit,result
        elif  ((topProfit - r ) * b )  >= 100 :
            #linePush(endTime.strftime("%Y-%m-%d %H:%M:%S") +' '+'強制出場+')
            #print('強制出場')
            r,b,result = OrderOut(df,r,b,endTime,result)
            return r,b ,topProfit,result
        #elif mp < lsp :
        #    print('苻合停損-')
        #    r,b = outp(df,r,b,1,i)
        
    elif b == 1 and  df['Close'].iloc[index] < df['BoxTop'].iloc[index]:
        #linePush(endTime.strftime("%Y-%m-%d %H:%M:%S") +' '+'苻合停損+出場')
            #print('苻合停損+')
        r,b,result = OrderOut(df,r,b,endTime,result)
        return r,b ,topProfit,result

    elif b == -1 and  df['Close'].iloc[index] > df['BoxDown'].iloc[index]:
        #linePush(endTime.strftime("%Y-%m-%d %H:%M:%S") +' '+'苻合停損-出場')
            #print('苻合停損-')
        r,b,result = OrderOut(df,r,b,endTime,result)
        return r,b ,topProfit,result
    
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
   
    return 0,0,result