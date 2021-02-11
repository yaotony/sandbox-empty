
#定義進場函數，呼號範例為(r,b) = inp(df,r,b,i)
def inp(df,r,b,i):
    isOk =False
    #r=成本 b=多空方設定 多方=1 空方=-1
    print(df['Open'].iloc[i])
    print(df['Close'].iloc[i-1])
    print(df['BoxTop'].iloc[i])
    
    if( b == 1 and  df['Close'].iloc[i] > df['Close'].iloc[i-1] and df['Close'].iloc[i] > df['BoxTop'].iloc[i-1]) :
        isOk = True
    elif( b == -1 and  df['Close'].iloc[i] < df['Close'].iloc[i-1] and df['Close'].iloc[i] < df['BoxDown'].iloc[i-1]) :
        isOk = True
    else :
        isOk =False
        b = 0

    
    if isOk == True :
        df['sign'].iloc[i] = b #進場時記錄多空
        r = df['Open'].iloc[i] #設定多方買進與空方賣出成本
        df['note'].iloc[i] =str(r) + df['note'].iloc[i]+ " 下單 ： " + str(b) +"  :  "
   
    return (r,b)


#定義出場函數，呼號範例為(r,b) = outp(df,r,b,price,i)
def outp(df,r,b,price,i):
    #r是資金存量，b=多空方設定 多方=1 空方=-1
    #price=1代表開盤價，price=4代表收盤價
    rr = (df['Open'].iloc[i] - r) * b
    df['ret'].iloc[i] = rr #進場時記錄多空
    df['note1'].iloc[i] = df['note1'].iloc[i] + ' 出場： b=' + str(b) +' ： 下單：' + str(r) +' , 出場：'+ str(df['Close'].iloc[i]) +' ,結算 ： '+str(rr)
    df['note'].iloc[i] = df['note'].iloc[i] +'出場：'+str(int(rr))
    r=0#歸零
    b=0#多空方歸零
    return (r,b)

#定義當日結算和停利停損函數
def stop(df,wsp,lsp,r,b,i,topProfit):
    #r是資金存量，b=多空方設定 多方=1 空方=1
    #mm = df.iloc[i,4] #當日結算(收盤價)
    #mp = mm / r  # 以當日結價價 / 進場成本
    #公式=(現價-上一交易日的收盤價)/上一交易日的收盤價X100%。
    
    mp = 0
    try:
        mm = df['Close'].iloc[i] 
        mp = ( (int(mm) - int(r)) / int(r) )  * 100 * b
        if(b == 1 and topProfit < mm) : 
            topProfit = mm
        elif (b == -1 and topProfit > mm) :
            topProfit = mm
        
        print('r:'+str(r))
        print('topProfit:'+str(topProfit))
    

        mp1 =  ( (int(mm) - int(topProfit)) / int(topProfit) )  * 100 * b

        print('mpV='+str( topProfit - r ) * b )
        print('mpV1='+str ( topProfit -  mm) * b )
        print('mpV2='+str (  ((topProfit - r ) * b ) * wsp  ))

        print('mp = ( int(mm) - int(r) / int(r) )  * 100 : ' +str(round(mp,2)) +' = ('+ str(int(mm)) +'-'+ str(int(r))+' / '+str(int(r))+')  * 100 * ' + str(b)  )
        print('mp1 = ( int(mm) - int(topProfit) / int(topProfit) )  * 100 : ' +str(round(mp1,2)) +' = ('+ str(int(mm)) +'-'+ str(int(topProfit))+' / '+str(int(topProfit))+')  * 100 * ' + str(b)  )
        df['AA'].iloc[i] = ((topProfit - r ) * b )
        df['BB'].iloc[i] = ((topProfit - r ) * b ) * wsp
        df['CC'].iloc[i] = ((topProfit - mm) * b )
        df['DD'].iloc[i] = mp
        #if mp > 0.1  :
        if ((topProfit - r ) * b ) * wsp < (topProfit - mm ) * b  :
            print('苻合停利')
            r,b = outp(df,r,b,1,i+1)       
        
        #elif mp < lsp :
        #    print('苻合停損')
        #    r,b = outp(df,r,b,1,i+1)
            

       
        
        #mp =  (df['Close'].iloc[i] - r ) * b 
        #若當日結算比率大於10%或小於5% 
    except :
        print('--------:'+str(r))
    
    


    
    #if  topProfit < lsp :
    #if  mp < lsp :
    #若苻合停利、停損條件，以下一筆開盤價出場
        #print('苻合停損')
       # r,b = outp(df,r,b,1,i+1)
    #df['note'].iloc[i] =df['note'].iloc[i] +' 停利、停損 MP = ' + str(mp) + '=' +  '('+str(df.iloc[i,4] ) +'-' + str(r)+ ') *'+str( b) 
        
   
    return (r,b,topProfit)
