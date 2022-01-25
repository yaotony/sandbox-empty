from LineMSG import send_message,send_bs_message,send_All_message

#定義進場函數，呼號範例為(r,b) = inp(df,r,b,i)
def inp(time,r,b,note,re,orV):

    note =note + " 下單 ： "+str(r) + ' : '+ str(b) + " Time:"+time.strftime('%Y-%m-%d %H:%M')
    print(note)
    re.append([time,r,r,r,0,b,0,0,note])
    orV.append([time,r,b,note])
    send_bs_message( note)
    return (r,b,re,orV)

def addInp(time,r,b,note,re,orV):

    note =note + " 加碼下單 ： "+str(r) + ' : '+ str(b) + " Time:"+time.strftime('%Y-%m-%d %H:%M')
    print(note)
    re.append([time,r,r,r,0,b,0,0,note])
    orV.append([time,r,b,note])
    send_bs_message( note)
    return (re,orV)



#定義出場函數，呼號範例為(r,b) = outp(df,r,b,price,i)
def outp(time,Price,r,b,note,re,orV):
     #r是資金存量，b=多空方設定 多方=1 空方=-1
    #price=1代表開盤價，price=4代表收盤價
    for i in range( len(orV)) :
        r= orV[i][1]
        rr = (Price - r) * b
        note = ' 出場： b=' + str(b) +' ： 下單：' + str(r) +' , 出場：'+ str(Price) +' ,結算 ： '+str(rr)+ " Time:"+time.strftime('%Y-%m-%d %H:%M')
        re.append([time,r,r,r,0,b,rr,0,note])
        print(note)
        #sendMSG(b,df['Time'].iloc[i],"Exit")
        send_bs_message( note)
        note =''
    
    #print(orV)
    r=0#歸零
    b=0#多空方歸零
    orV =[]

    return (r,b,rr,re,orV)

#定義當日結算和停利停損函數
def stop(time,Price,wsp,lsp,r,b,topProfit,note,re,orV):
    #r是資金存量，b=多空方設定 多方=1 空方=1
    #mm = df.iloc[i,4] #當日結算(收盤價)
    #mp = mm / r  # 以當日結價價 / 進場成本
    #公式=(現價-上一交易日的收盤價)/上一交易日的收盤價X100%。
   # if b == 1 :
   #     topProfit = df['High'].iloc[i].rolling(5).max()
   # elif b == -1 : 
   #     topProfit = df['Low'].iloc[i].rolling(5).min()     
        mp = 0
        rr = 0
        rrr = r
        bb = b
        mp1 =(((topProfit - r ) * b ) * wsp)
        mp2 =(topProfit - Price ) * b

        if(b == 1 and topProfit < Price) : 
            topProfit = Price
        elif (b == -1 and topProfit > Price) :
            topProfit = Price


   

        if   ( int(Price) - int(r) ) > 0 :# and r > 0:#mm > 0 and r > 0: #
            #mp = ( (int(Price) - int(r)) / int(r) )  * 100 * b
            
           
            #print('(Price - r) * b =',str((Price - r) * b))
            
            if ((topProfit - r ) * b ) > 0 and ((Price - r ) * b) > 10  :# mp > wsp:# (((topProfit - r ) * b ) * wsp) < (topProfit - mm ) * b :
                    #print('苻合停利+')
                if (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b :
                    r,b,rr,reValues = outp(time,Price,r,b,note,re,orV) 
                       
            elif    ((topProfit - Price) * b ) >= 10 :
                #         print('強制出場')
                r,b,rr,reValues = outp(time,Price,r,b,note,re,orV)
                 
        elif b == 1 and ((topProfit - Price) * b ) >= 10 :#((r - Price) * b ) >= 10 :
            r,b,rr,reValues = outp(time,Price,r,b,note,re,orV)
            
 
            
              
        
        #note =  note +' mp:'+str(mp)  + ' r:'+str(rrr)  + ' b:'+str(bb)  + ' wsp:'+str(wsp)  + ' Price:'+str(Price)  +  'topProfit:'+str(topProfit)  + '  (((topProfit - r ) * b ) * wsp) ='+ str(mp1) +'  (topProfit - mm ) * b='+str(mp2)
                
        return (r,b,rr,topProfit,re,note)

def stopByMA(time,Price,wsp,lsp,r,b,topProfit,note,re,pf,KBar1M,orV,aorV):
    #r是資金存量，b=多空方設定 多方=1 空方=1
    #mm = df.iloc[i,4] #當日結算(收盤價)
    #mp = mm / r  # 以當日結價價 / 進場成本
    #公式=(現價-上一交易日的收盤價)/上一交易日的收盤價X100%。
   # if b == 1 :
   #     topProfit = df['High'].iloc[i].rolling(5).max()
   # elif b == -1 : 
   #     topProfit = df['Low'].iloc[i].rolling(5).min()    
        FastPeriod=10
        SlowPeriod=30  
        mp = 0
        rr = 0
        rrr = r
        bb = b
        mp1 =(((topProfit - r ) * b ) * wsp)
        mp2 =(topProfit - Price ) * b

        if(b == 1 and topProfit < Price) : 
            topProfit = Price
        elif (b == -1 and topProfit > Price) :
            topProfit = Price

        BoxTop =pf['BoxTop'].iloc[1] 
        BoxDown =pf['BoxDown'].iloc[1] 
        #FastMA=KBar1M.GetMAByOpen(FastPeriod,0)
        #SlowMA=KBar1M.GetMAByOpen(SlowPeriod,0)
        #Last1FastMA,Last2FastMA=FastMA[-2],FastMA[-1]
        #Last1SlowMA,Last2SlowMA=SlowMA[-2],SlowMA[-1]
        Last1FastMA,Last2FastMA=pf['ma_s'].iloc[2],pf['ma_s'].iloc[1]
        Last1SlowMA,Last2SlowMA=pf['ma_l'].iloc[2],pf['ma_l'].iloc[1]  
        Last1_40MA,Last2_40MA=pf['ma_40'].iloc[3],pf['ma_40'].iloc[1]
        Last1_Close,Last2_Close=pf['close'].iloc[3],pf['close'].iloc[1] 

        bb =0 
        bc = 0
    #     if  BoxTop < Last2FastMA  :#and BoxTop < Last2SlowMA :
    #         bb = 1   
    #     elif  BoxDown > Last2FastMA :# and BoxDown > Last2SlowMA :   
    #         bb = -1

    
        # if b==1 and  Last1_Close  >  Last2_40MA  and  Last2_Close < Last2_40MA and (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b  :
        #     bb = -1
        #     print('多單提早出場MA40')
        # elif b==-1 and Last1_Close  <  Last2_40MA  and  Last2_Close > Last2_40MA and (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b   :
        #     bb =1
        #     print('空單提早出場MA40')
        if  Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA and (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b :#pf['ma_sign'].iloc[-1] == 1:
            bb = 1      
        elif Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA and (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b :# pf['ma_sign'].iloc[-1] == -1:
            bb = -1 
        # elif   b==1 and (Price - max(orV,key = lambda x:x[1])[1] * b) < -50 :
        #     bb = -1 
        #     print('多 單提早出場',(((topProfit - max(orV,key = lambda x:x[1])[1] ) * b ) * -0.2),(topProfit - Price ) * b)
        # elif    b==-1 and (Price - min(orV,key = lambda  x:x[1])[1]  ) * b < -50 :
        #     bb = 1
        #     print('空 單提早出場',(((topProfit - min(orV,key = lambda  x:x[1])[1]  ) * b ) * -0.2) , (topProfit - Price ) * b )  
        # elif len(orV) >= 2 and b==1 and Price < max(orV,key = lambda x:x[1])[1] and (((topProfit - max(orV,key = lambda x:x[1])[1] ) * b ) * -0.2) < (topProfit - Price ) * b :
        #    bb = -1 
        #    print('多單提早出場',(((topProfit - max(orV,key = lambda x:x[1])[1] ) * b ) * -0.2),(topProfit - Price ) * b)
        # elif  len(orV) >= 2 and  b==-1 and Price > min(orV,key = lambda  x:x[1])[1]  and (((topProfit - min(orV,key = lambda  x:x[1])[1]  ) * b ) * -0.2) < (topProfit - Price ) * b :
        #    bb = 1
        #    print('空 單提早出場',(((topProfit - min(orV,key = lambda  x:x[1])[1]  ) * b ) * -0.2) , (topProfit - Price ) * b )  
        else  :
            if  Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA and  b==1 :
                print('黃金交叉 - 加碼做多')
                note='黃金交叉 - 加碼做多'
                bc = 1
                # if b==-1 and Price > min(orV,key = lambda  x:x[1])[1]  and (((topProfit - min(orV,key = lambda  x:x[1])[1]  ) * b ) * wsp) < (topProfit - Price ) * b :
                #      bb=1
                #      print('空單提早出場',(((topProfit - max(orV,key = lambda x:x[1])[1] ) * b ) * wsp),(topProfit - Price ) * b)

            elif Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA and b==-1 :
                print('死亡交叉 - 加碼做空')
                note='死亡交叉 - 加碼做空'
                bc = -1
            #     if b==1 and Price < max(orV,key = lambda  x:x[1])[1]  and (((topProfit - max(orV,key = lambda  x:x[1])[1]  ) * b ) * wsp) < (topProfit - Price ) * b :
            #          bb = -1
            #          print('多 單提早出場',(((topProfit - min(orV,key = lambda  x:x[1])[1]  ) * b ) * wsp) , (topProfit - Price ) * b )
            elif  BoxTop > Last1FastMA  and BoxTop < Last2FastMA and b==1 :
                print('突破箱頂 - 加碼做多')
                note='突破箱頂 - 加碼做多'
                bc = 1
                # if b==-1 and Price > min(orV,key = lambda  x:x[1])[1]  and (((topProfit - min(orV,key = lambda  x:x[1])[1]  ) * b ) * wsp) < (topProfit - Price ) * b :
                #      bb=1
                #      print('空單提早出場',(((topProfit - max(orV,key = lambda x:x[1])[1] ) * b ) * wsp),(topProfit - Price ) * b)
           
            elif  BoxDown < Last1FastMA     and BoxDown > Last2FastMA  and b==-1:  
                print('突破箱底 - 加碼做空')
                note='突破箱底 - 加碼做空'
                bc = -1
                # if b==1 and Price < max(orV,key = lambda  x:x[1])[1]  and (((topProfit - max(orV,key = lambda  x:x[1])[1]  ) * b ) * wsp) < (topProfit - Price ) * b :
                #      bb = -1
                #      print('多 單提早出場',(((topProfit - min(orV,key = lambda  x:x[1])[1]  ) * b ) * wsp) , (topProfit - Price ) * b )

     
     #   if  b== 1 and Price < Last2FastMA and  (Price - r) * b < -40 :
     #       bb = -1
     #   elif  b== -1 and Price > Last2FastMA and (Price - r) * b < -40:
     #       bb =1
        

            
        if bb !=0  and bb != b:
            aorV[-1][2]=b 
            aorV[-1][3]=note 
            r,b,rr,re,orV = outp(time,Price,r,b,note,re,orV)
           
        elif bc == b:
            #print('max(orV,key = lambda x:x[1])',max(orV,key = lambda x:x[1])[1])
            #目前價格有大於最後加碼價才可以加碼：
            if (b == 1 and Price > max(orV,key = lambda x:x[1])[1]) or (b == -1 and Price < min(orV,key = lambda  x:x[1])[1]) :
                #if len(orV) < 4 :
                    re,orV = addInp(time,Price,b,note,re,orV)
                    aorV[-1][2]=b 
                    aorV[-1][3]=note
                    print('Add')

            

        
            
              
        
     #   note =  note +' mp:'+str(mp)  + ' r:'+str(rr)  + ' b:'+str(bb)  + ' wsp:'+str(wsp)  + ' Price:'+str(Price)  +  'topProfit:'+str(topProfit)  + '  (((topProfit - r ) * b ) * wsp) ='+ str(mp1) +'  (topProfit - mm ) * b='+str(mp2)
                
        return (r,b,rr,topProfit,re,orV,aorV)
