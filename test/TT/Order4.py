import time ,datetime

#定義進場函數，呼號範例為(r,b) = inp(df,r,b,i)
def inp(time,r,b,note,re):

    note =note + " 下單 ： "+str(r) + ' : '+ str(b) + " Time:"+time.strftime('%Y-%m-%d %H:%M')
    print(note)
    re.append([time,r,r,r,0,b,0,0,note])
    note =''
    return (r,b,note,re)



#定義出場函數，呼號範例為(r,b) = outp(df,r,b,price,i)
def outp(time,Price,r,b,note,re):
    #r是資金存量，b=多空方設定 多方=1 空方=-1
    #price=1代表開盤價，price=4代表收盤價
    rr = (Price - r) * b
    note = note + ' 出場： b=' + str(b) +' ： 下單：' + str(r) +' , 出場：'+ str(Price) +' ,結算 ： '+str(rr)+ " Time:"+time.strftime('%Y-%m-%d %H:%M')
    re.append([time,r,r,r,0,b,rr,0,note])
    print(note)
    #sendMSG(b,df['Time'].iloc[i],"Exit")
    r=0#歸零
    b=0#多空方歸零
    note =''
    #linePush( df['note1'].iloc[i])
    return (r,b,rr,note,re)

#定義當日結算和停利停損函數
def stopByS(time,Price,wsp,lsp,r,b,sr,sb,topProfit,note,re):
  
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
        
        pointTime = datetime.datetime.strptime( time.strftime('%Y-%m-%d')  +' 12:50:00','%Y-%m-%d %H:%M:%S')


        if   ( int(Price) - int(r) ) > 0 :# and r > 0:#mm > 0 and r > 0: #
            
            # if sb == 0  and (Price - r) * b < 0:
            #          sr,sb,note = inp(Price,1,note)
            #          print('1 保險進場： sr= ',sr,' sb=',sb,' (Price - r)',(Price - r),' Time:',time )   
            #          note = '保險單- '+note
             
            #if sb == 0 and  ((topProfit - Price) * b ) >= 30 :
            #        sr,sb,note,re = inp(time,Price,1,note,re)
            
            if  ((topProfit - Price) * b ) >= 20 :
                #         print('強制出場')
                r,b,rr,note,re = outp(time,Price,r,b,note,re)
                note = note +'強制出場+lsp < mp'  
                #print('強制出場 - ((topProfit - Price) * b )',((topProfit - Price) * b ),' topProfit=',topProfit,'  Price=',Price )
                if sb!=0 :
                    note = '保險單- '              
                    sr,sb,srr,note,re = outp(time,Price,sr,sb,note,re)
                    #print('保險出場： sr= ',sr,' sb=',sb,'  srr=',srr,' Time:',time )
 
        else :
 
                if ((topProfit - r ) * b ) > 20  and  (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b:
                    # print(' (((topProfit - r ) * b ) * wsp=) ', (((topProfit - r ) * b ) * wsp)  )
                    # print('(topProfit - Price ) * b =', (topProfit - Price ) * b  )
                    # print('topProfit=',topProfit)
                    # print('Price=',Price)
                    # print('r=',r)
                    note = '保險單- '
                    r,b,rr,note,re = outp(time,Price,r,b,note,re) 
                    #sr,sb,note,re = inp(time,Price,1,note,re)
                    #print('1 保險進場： sr= ',sr,' sb=',sb,' (Price - r)',(Price - r),' Time:',time )
                

                # if  (Price - r) * b >= 200 :
               #     
                #     print('停利出場 - ((topProfit - Price) * b )',((topProfit - Price) * b ),' topProfit=',topProfit,'  Price=',Price )

                #     if sb!=0 :                
                #         sr,sb,srr,note,re = outp(time,Price,sr,sb,note,re)
                #         print('保險出場： sr= ',sr,' sb=',sb,'  srr=',srr,' Time:',time )   
            
              
        
        note =  note +' mp:'+str(mp)  + ' r:'+str(rrr)  + ' b:'+str(bb)  + ' wsp:'+str(wsp)  + ' Price:'+str(Price)  +  'topProfit:'+str(topProfit)  + '  (((topProfit - r ) * b ) * wsp) ='+ str(mp1) +'  (topProfit - mm ) * b='+str(mp2)
                
        return (r,b,sr,sb,topProfit,rr,srr,note,re)


def stopByB(time,Price,wsp,lsp,r,b,sr,sb,topProfit,note,re):
  
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
                    
            
 
            if  ((topProfit - Price) * b ) >= 20 :
                #print('強制出場 - ((topProfit - Price) * b )',((topProfit - Price) * b ),' topProfit=',topProfit,'  Price=',Price )
                r,b,rr,note,re = outp(time,Price,r,b,note,re)
                note = note +'強制出場+lsp < mp'
                if sb!=0 :
                    note = '保險單- '                
                    sr,sb,srr,note,re = outp(time,Price,sr,sb,note,re)
                    #print('保險出場： sr= ',sr,' sb=',sb,'  srr=',srr,' Time:',time )  
        else  :
          

            if ((topProfit - r ) * b ) > 20 and  (((topProfit - r ) * b ) * wsp) < (topProfit - Price ) * b:
                    # print(' (((topProfit - r ) * b ) * wsp=) ', (((topProfit - r ) * b ) * wsp)  )
                    # print('(topProfit - Price ) * b =', (topProfit - Price ) * b  )
                    # print('topProfit=',topProfit)
                    # print('Price=',Price)
                    # print('r=',r)
                    note = '保險單- '
                    r,b,rr,note,re = outp(time,Price,r,b,note,re)
                    #print('停利出場 - ((topProfit - Price) * b )',((topProfit - Price) * b ),' topProfit=',topProfit,'  Price=',Price )

                    #sr,sb,note,re = inp(time,Price,-1,note,re)
           
                    #print('-1 保險進場： sr= ',sr,' sb=',sb,' (Price - r)',(Price - r),' Time:',time )

            #print(' Time:',time,' (Price - r) =', (Price - r) ,' Price=',Price,' r=',r)

            # if  (Price - r) * b >= 200 :
            #     r,b,rr,note,re = outp(time,Price,r,b,note,re)
            #     print('停利出場 - ((topProfit - Price) * b )',((topProfit - Price) * b ),' topProfit=',topProfit,'  Price=',Price )

            #     if sb!=0 :                
            #         sr,sb,srr,note,re = outp(time,Price,sr,sb,note,re)
            #         print('保險出場： sr= ',sr,' sb=',sb,'  srr=',srr,' Time:',time )   
                
        
        note =  note +' mp:'+str(mp)  + ' r:'+str(rrr)  + ' b:'+str(bb)  + ' wsp:'+str(wsp)  + ' Price:'+str(Price)  +  'topProfit:'+str(topProfit)  + '  (((topProfit - r ) * b ) * wsp) ='+ str(mp1) +'  (topProfit - mm ) * b='+str(mp2)
                
        return (r,b,sr,sb,topProfit,rr,srr,note,re)