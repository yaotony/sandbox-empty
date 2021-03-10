

#定義進場函數，呼號範例為(r,b) = inp(df,r,b,i)
def inp(r,b,note):

    note = " 下單 ： "+str(r) + ' : '+ str(b) 
   
    return (r,b,note)


#定義出場函數，呼號範例為(r,b) = outp(df,r,b,price,i)
def outp(Price,r,b,note):
    #r是資金存量，b=多空方設定 多方=1 空方=-1
    #price=1代表開盤價，price=4代表收盤價
    rr = (Price - r) * b
    note =' 出場： b=' + str(b) +' ： 下單：' + str(r) +' , 出場：'+ str(Price) +' ,結算 ： '+str(rr)
    print(note)
    #sendMSG(b,df['Time'].iloc[i],"Exit")
    r=0#歸零
    b=0#多空方歸零
    #linePush( df['note1'].iloc[i])
    return (r,b,rr,note)

#定義當日結算和停利停損函數
def stop(Price,wsp,lsp,r,b,topProfit,note):
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
                    r,b,rr,note = outp(Price,r,b,note)   
                    note = note +'苻合停利+'   
            elif    ((topProfit - Price) * b ) >= 10 :
                #         print('強制出場')
                r,b,rr,note = outp(Price,r,b,note)
                note = note +'強制出場+lsp < mp'  
        elif b == 1 and ((topProfit - Price) * b ) >= 10 :#((r - Price) * b ) >= 10 :
            r,b,rr,note = outp(Price,r,b,note)
            note = note +'強制出場+' 
        #elif b == -1  :
        #    mp = ( (int(Price) - int(r)) / int(r) )  * 100 * b
        #    if mp > wsp :# mp > wsp:# (((topProfit - r ) * b ) * wsp) < (topProfit - mm ) * b :
        #             #print('苻合停利+')
                #if (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b :
        #            r,b,rr,note = outp(Price,r,b,note)   
        #            note = note +'苻合停利+'  
        # elif b == -1  and ( int(Price) - int(r) ) < 0 :
        #     mp = ( (int(Price) - int(r)) / int(r) )  * 100 * b
            
        #     if ((topProfit - r ) * b ) > 0 and ((Price - r ) * b) > 10  :# mp > wsp:# (((topProfit - r ) * b ) * wsp) < (topProfit - mm ) * b :
        #             #print('苻合停利+')
        #         if (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b :
        #             r,b,rr,note = outp(Price,r,b,note)   
        #             note = note +'苻合停利+'   
        #     elif  ((topProfit - Price) * b ) >= 10 :
        #         #         print('強制出場')
        #         r,b,rr,note = outp(Price,r,b,note)
        #         note = note +'強制出場+'  
        # else :
        #         if  ((topProfit - Price) * b ) >= 10 :
        # #         #         print('強制出場')
        #             r,b,rr,note = outp(Price,r,b,note)
        #             note = note +'強制出場+++'
        # # elif b == -1  and ( int(Price) - int(r) ) > 0 :
        # #         if  ((topProfit - Price) * b ) >= 10 :
        # #         #         print('強制出場')
        # #             r,b,rr,note = outp(Price,r,b,note)
        # #             note = note +'強制出場+'
            
              
        
        note =  note +' mp:'+str(mp)  + ' r:'+str(rrr)  + ' b:'+str(bb)  + ' wsp:'+str(wsp)  + ' Price:'+str(Price)  +  'topProfit:'+str(topProfit)  + '  (((topProfit - r ) * b ) * wsp) ='+ str(mp1) +'  (topProfit - mm ) * b='+str(mp2)
                
        return (r,b,topProfit,rr,note)
