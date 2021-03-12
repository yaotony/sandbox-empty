

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
def stopByS(Price,wsp,lsp,r,b,sr,sb,topProfit,note,time):
  
        mp = 0
        rr = 0
        srr =0
        rrr = r
        bb = b
        mp1 =(((topProfit - r ) * b ) * wsp)
        mp2 =(topProfit - Price ) * b

        if(b == 1 and topProfit < Price) : 
            topProfit = Price
        elif (b == -1 and topProfit > Price) :
            topProfit = Price
        mp = ( (int(Price) - int(r)) / int(r) )  * 100 * b


        if   ( int(Price) - int(r) ) > 0 :# and r > 0:#mm > 0 and r > 0: #
            
            # if sb == 0  and (Price - r) * b < 0:
            #          sr,sb,note = inp(Price,1,note)
            #          print('1 保險進場： sr= ',sr,' sb=',sb,' (Price - r)',(Price - r),' Time:',time )   
            #          note = '保險單- '+note

            if  ((topProfit - Price) * b ) >= 50 :
                #         print('強制出場')
                r,b,rr,note = outp(Price,r,b,note)
                note = note +'強制出場+lsp < mp'  
                print('強制出場 - ((topProfit - Price) * b )',((topProfit - Price) * b ),' topProfit=',topProfit,'  Price=',Price )
                if sb!=0 :              
                    sr,sb,srr,note = outp(Price,sr,sb,note)
                    print('保險出場： sr= ',sr,' sb=',sb,'  srr=',srr,' Time:',time )
 
        else :
                if sb == 0 and   ((topProfit - r ) * b ) > 10 and  (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b:
                    # print(' (((topProfit - r ) * b ) * wsp=) ', (((topProfit - r ) * b ) * wsp)  )
                    # print('(topProfit - Price ) * b =', (topProfit - Price ) * b  )
                    # print('topProfit=',topProfit)
                    # print('Price=',Price)
                    # print('r=',r)
                    sr,sb,note = inp(Price,1,note)
                    print('1 保險進場： sr= ',sr,' sb=',sb,' (Price - r)',(Price - r),' Time:',time )

                if mp > wsp :# mp > wsp:# (((topProfit - r ) * b ) * wsp) < (topProfit - mm ) * b :
                    #print('苻合停利+')
                    if (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b :
#                       r,b,rr,note = outp(Price,r,b,note)   
                        note = note +'苻合停利+'          
            
              
        
        note =  note +' mp:'+str(mp)  + ' r:'+str(rrr)  + ' b:'+str(bb)  + ' wsp:'+str(wsp)  + ' Price:'+str(Price)  +  'topProfit:'+str(topProfit)  + '  (((topProfit - r ) * b ) * wsp) ='+ str(mp1) +'  (topProfit - mm ) * b='+str(mp2)
                
        return (r,b,sr,sb,topProfit,rr,srr,note)


def stopByB(Price,wsp,lsp,r,b,sr,sb,topProfit,note,time):
  
        mp = 0
        rr = 0
        rrr = r
        srr =0
        bb = b
        mp1 =(((topProfit - r ) * b ) * wsp)
        mp2 =(topProfit - Price ) * b

        if(b == 1 and topProfit < Price) : 
            topProfit = Price
        elif (b == -1 and topProfit > Price) :
            topProfit = Price

        mp = ( (int(Price) - int(r)) / int(r) )  * 100 * b
       
        if   ( int(Price) - int(r) ) < 0 :# and r > 0:#mm > 0 and r > 0: #
            #print('-----------------------------------------------------')

            # if sb ==  0 and (Price - r) * b < 0:
            #         sr,sb,note = inp(Price,-1,note)
            #         print('-1 保險進場： sr= ',sr,' sb=',sb,' (Price - r)',(Price - r),' Time:',time )  
                    
            
 
            if  ((topProfit - Price) * b ) >= 50 :
                print('強制出場 - ((topProfit - Price) * b )',((topProfit - Price) * b ),' topProfit=',topProfit,'  Price=',Price )
                r,b,rr,note = outp(Price,r,b,note)
                note = note +'強制出場+lsp < mp'
                if sb!=0 :                
                    sr,sb,srr,note = outp(Price,sr,sb,note)
                    print('保險出場： sr= ',sr,' sb=',sb,'  srr=',srr,' Time:',time )  
        else  :
           
            if sb == 0 and ((topProfit - r ) * b ) > 10 and  (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b:
                    # print(' (((topProfit - r ) * b ) * wsp=) ', (((topProfit - r ) * b ) * wsp)  )
                    # print('(topProfit - Price ) * b =', (topProfit - Price ) * b  )
                    # print('topProfit=',topProfit)
                    # print('Price=',Price)
                    # print('r=',r)
                    sr,sb,note = inp(Price,-1,note)
                    print('-1 保險進場： sr= ',sr,' sb=',sb,' (Price - r)',(Price - r),' Time:',time )

            #print(' Time:',time,' (Price - r) =', (Price - r) ,' Price=',Price,' r=',r)

            if mp > wsp :# mp > wsp:# (((topProfit - r ) * b ) * wsp) < (topProfit - mm ) * b :
                    #print('苻合停利+')
                if (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b :
#                   r,b,rr,note = outp(Price,r,b,note)   
                   note = note +'苻合停利+'  
                
        
        note =  note +' mp:'+str(mp)  + ' r:'+str(rrr)  + ' b:'+str(bb)  + ' wsp:'+str(wsp)  + ' Price:'+str(Price)  +  'topProfit:'+str(topProfit)  + '  (((topProfit - r ) * b ) * wsp) ='+ str(mp1) +'  (topProfit - mm ) * b='+str(mp2)
                
        return (r,b,sr,sb,topProfit,rr,srr,note)