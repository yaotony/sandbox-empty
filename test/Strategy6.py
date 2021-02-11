#1313
from Order import inp,outp,stop
from StrategyOBV import OBVTheory
from StrategyMA import MA

#RSI 策略
def RSI(d,df):
    #以今天的收盤價 - 前一天的收盤價，算出一個序列，命名為x
        x = df['Close'].iloc[:].diff() #計算前後項資料改變值
        #df['rsi_v'] =x 
     #先獎 x 中之於 0 值設為 0 ，然後每 d 天對 x 取平均
     #再將 x 中負值改為正值，然後每 d 天對 x 取平均
     #將兩個平均相除後*100 ， 算出一個序列，並把不符合條件的值指定其他數值
        #df['rsi_up']= x.where(x>0,0).rolling(d).mean() 
        #df['rsi_dn']= x.where(x>0,-x).rolling(d).mean()
        df['rsi']=100 * x.where(x>0,0).rolling(d).mean() / x.where(x>0,-x).rolling(d).mean()
    #RIS 交易訊號欄
        df['rsi_sign'] = 0
    #設定RSI指標超賣訊號= 0 (部位買進)
    #設定RSI指標超買訊號= -1 (部位買進)
        for i in  range( len(df)):
            if df['rsi'].iloc[i] > 90 :
                df['rsi_sign'] = -1
            elif df['rsi'].iloc[i] <  20 :
                df['rsi_sign'].iloc[i] = 1


    

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
   
    #Box 交易訊號欄
    df['box_sign'] =0
   
    

    df['BoxTopD'] = df['High'].iloc[:].rolling(N).max()
    df['BoxDownD'] = df['Close'].iloc[:].rolling(N).min()
    df['BoxTopN'] = df['High'].iloc[:].shift(1+N).rolling(N).max()
    df['BoxDownN'] = df['Close'].iloc[:].shift(1+N).rolling(N).min()

    OBVTheory(df,5,10) 
    MA(3,5,df)
    RSI(5,df)

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

        df['BoxTopDef'].iloc[i] = (df['BoxTop'].iloc[i] - df['Close'].iloc[i]) * -1
        df['BoxDownDef'].iloc[i] = df['BoxDown'].iloc[i] - df['Close'].iloc[i]

      
        
        #設定Box 指標箱型突破高點訊號= 1 (部位買進)
        if (df['BoxTop'].iloc[i] < df['Close'].iloc[i] ) &  (df['BoxTopDef'].iloc[i] > S) & (df['ma_s'].iloc[i] < df['Close'].iloc[i]) & (df['rsi'].iloc[i] < 90  and df['rsi'].iloc[i] > 15) :
            df['box_sign'].iloc[i] = 1
           
    
        
        #設定Box指標箱型突破低點訊號= -1 (部位買進)
        if (df['BoxDown'].iloc[i] > df['Close'].iloc[i])  &  (df['BoxDownDef'].iloc[i] > S ) & (df['ma_s'].iloc[i] > df['Close'].iloc[i]) & (df['rsi'].iloc[i] < 90  and df['rsi'].iloc[i] > 15) : 
            df['box_sign'].iloc[i] = -1
            



    #進行買賣
    K = 10 #設定保留K線參數
    L = len(df) #取得筆數
    r=0 #記錄交易資金流量
    b=0 #設定多空方，多方=1，空方=-1，空手=0
    df['sign']=0 #新增欄位，用來記錄進場多空
    df['ret']=0 #新增欄位，用來記錄出勤結算
    df['note']='' #記錄交易指數
    df['note1']='' #記錄交易指數

    #由於序號從0開始，迴圈從第k-1筆記錄開始執行

    c = 1  #  停利 = 1 停損 = -1

    for i in range(K-1,L):
    
        #若 i < 最後一筆，則執行
        if i < L-1 :
            #若 b = 1 ,表示多
            if b == 1 :
                if df['ma_sign'].iloc[i] == -1 :
                    (r,b) = outp(df,r,b,1,i+1)
                else :
                    (r,b,c)=stop(df,25,-20,r,b,i)
                #if df['BoxDown'].iloc[i]  > df['Close'].iloc[i]+50  :# or (df['Close'].iloc[i]+20  < df['BoxTop'].iloc[i]  and   df['Close'].iloc[i]+20   < df['BoxDown'].iloc[i]) : 
                #    df['note1'].iloc[i] =df['note1'].iloc[i] + 'A-: '+ str(df['BoxDown'].iloc[i]) +' > ' + str(df['Close'].iloc[i]+50)
                #    (r,b) = outp(df,r,b,1,i+1)
                #else :#停利、停損
                #    df['note1'].iloc[i] =df['note1'].iloc[i] + 'B'
                #    (r,b,c)=stop(df,50,-50,r,b,i)
                    
            elif b == -1 :
                if df['ma_sign'].iloc[i]  == 1 :
                    (r,b) = outp(df,r,b,1,i+1)
                else :
                    (r,b,c)=stop(df,25,-20,r,b,i)
                #if  df['BoxTop'].iloc[i] < df['Close'].iloc[i]-50   :#or  (df['Close'].iloc[i]-20 > df['BoxTop'].iloc[i]  and   df['Close'].iloc[i]-20  > df['BoxDown'].iloc[i] ) : 
                #    df['note1'].iloc[i] =df['note1'].iloc[i] + 'A-: '+ str(df['BoxTop'].iloc[i]) +' <' + str(df['Close'].iloc[i]-50)
                #    (r,b) = outp(df,r,b,1,i+1)
                #else :#停利、停損
                #    df['note1'].iloc[i] =df['note1'].iloc[i] + 'B'
                #    (r,b,c)=stop(df,50,-50,r,b,i)
                   
            
                #若b=0,表示空手
            elif b == 0 :
                if  df['ma_sign'].iloc[i] == 1 :
                    r,b = inp(df,r,1,i+1) 
                    #if df['rsi_sign'].iloc[i] == 0 :
                    #    r,b = inp(df,r,1,i+1)
                    #else :
                    #    r,b = inp(df,r,df['rsi_sign'].iloc[i],i+1)
                    
                  
                elif  df['ma_sign'].iloc[i] == -1 : 
                    r,b = inp(df,r,-1,i+1)
                    #if df['rsi_sign'].iloc[i] == 0 :
                    #    r,b = inp(df,r,-1,i+1)
                    #else :
                    #    r,b = inp(df,r,df['rsi_sign'].iloc[i],i+1)
                    
                
                 
        elif i == L-1 :
            #若b不等於0 (表示還有部位)
            if b != 0 :
                (r,b) = outp(df,r,b,4,i)