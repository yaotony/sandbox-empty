import pandas as pd

# MA策略 黃金交叉 = 1   死亡交叉 = -1  預設=0
def MA(s,l,df):
    #平均線產生
    df['ma_s'] = df.iloc[:,4].rolling(s).mean()#以收盤價[close]計算5日均線 
    df['ma_l'] = df.iloc[:,4].rolling(l).mean()#以收盤價[close]計算5日均線 
    #MA 交易訊號欄
    df['ma_sign']=0
    #設定黃金交叉訊號
    df['ma_sign'][(df['ma_s'].shift(1) < df['ma_l'].shift(1)) & (df['ma_s'] > df['ma_l']) ]=1
    #設定死亡交叉訊號
    df['ma_sign'][(df['ma_s'].shift(1) > df['ma_l'].shift(1)) & (df['ma_s'] < df['ma_l']) ]=-1
  
#RSI 策略
def RSI(d,df):
    #以今天的收盤價 - 前一天的收盤價，算出一個序列，命名為x
        x = df.iloc[:,4].diff() #計算前後項資料改變值
        #df['rsi_v'] =x 
     #先獎 x 中之於 0 值設為 0 ，然後每 d 天對 x 取平均
     #再將 x 中負值改為正值，然後每 d 天對 x 取平均
     #將兩個平均相除後*100 ， 算出一個序列，並把不符合條件的值指定其他數值
        #df['rsi_up']= x.where(x>0,0).rolling(d).mean() 
        #df['rsi_dn']= x.where(x>0,-x).rolling(d).mean()
        df['rsi']=100 * x.where(x>0,0).rolling(d).mean() / x.where(x>0,-x).rolling(d).mean()
    #RIS 交易訊號欄
        df['rsi_sign'] =0
    #設定RSI指標超賣訊號= 0 (部位買進)
        df['rsi_sign'][(df['rsi']<10)]= 1
    #設定RSI指標超買訊號= -1 (部位買進)
        df['rsi_sign'][(df['rsi']>90)]= -1


#定義進場函數，呼號範例為(r,b) = inp(df,r,b,i)
def inp(df,r,b,i):
    #r=成本 b=多空方設定 多方=1 空方=1
    df['sign'].iloc[i] = b #進場時記錄多空
    r = df.iloc[i,1] #設定多方買進與空方賣出成本
    df['note'].iloc[i] =str(r) + df['note'].iloc[i]+ " 下單 ： " + str(b) +"  :  "

    return (r,b)


#定義出場函數，呼號範例為(r,b) = outp(df,r,b,price,i)
def outp(df,r,b,price,i):
    #r是資金存量，b=多空方設定 多方=1 空方=-1
    #price=1代表開盤價，price=4代表收盤價
    rr = (df.iloc[i,1] - r) * b
    df['ret'].iloc[i] = rr #進場時記錄多空
    df['note'].iloc[i] = df['note'].iloc[i] +'出場： b=' + str(b) +' ： 下單：' + str(r) +' , 出場：'+ str(df.iloc[i,1]) +' ,結算 ： '+str(rr)
    r=0#歸零
    b=0#多空方歸零
    return (r,b)

#定義當日結算和停利停損函數
def stop(df,wsp,lsp,r,b,i):
    #r是資金存量，b=多空方設定 多方=1 空方=1
    #mm = df.iloc[i,4] #當日結算(收盤價)
    #mp = mm / r  # 以當日結價價 / 進場成本
    mp =  (df.iloc[i,4] - r ) * b 
        #若當日結算比率大於10%或小於5% 
    if mp > wsp or mp < lsp :
        #若苻合停利、停損條件，以下一筆開盤價出場

        df['note'].iloc[i] =df['note'].iloc[i] +' 停利、停損 MP = ' + str(mp) + '=' +  '('+str(df.iloc[i,4] ) +'-' + str(r)+ ') *'+str( b) 
        r,b = outp(df,r,b,1,i+1)
    return (r,b)


def BoxTheory(df,N):
    #當近期N天內的高點比 N+1 天前的 N天內高點還低時 ,則 N+1天前的 N天內高點 為近期箱型的頂部。
    #當近期M天內的低點比 M+1 天前的 M天內低點還高時 ,則 M+1天前的 M天內低點 為近期箱型的底部。
    df['BoxTop']  = 0
    df['BoxDown'] = 0
    #Box 交易訊號欄
    df['box_sign'] =0

    df['BoxTop'] = df.iloc[:,2].shift(1).rolling(N).max()
    df['BoxDown'] = df.iloc[:,2].shift(1).rolling(N).min()


    #設定Box 指標箱型突破高點訊號= 1 (部位買進)
    df['box_sign'][(df['BoxTop'] < df['Close'])]= 1
    #設定Box指標箱型突破低點訊號= -1 (部位買進)
    df['box_sign'][(df['BoxDown'] > df['Close'])]= -1




#計算各項策略績效指標
#df為欲分析策略績效的資料
def result_F(df):
    #計算最後報酬
    last = df['cus'].iloc[-1]
    #計算交易次數
    count = df['sign'][df['sign']!=0].count()
    wamt = df['ret'][df['ret']>0].sum()
    lamt = df['ret'][df['ret']<0].sum()
    
    #計算最大回檔
    def maxdrawdown(s):
        s = s.cummax() - s #歷史最高價 - 現在序列,cummax 生成當日之前的歷史最高價序列
        return (s.max())
    
    mdd = maxdrawdown(df['cus'])
    #計算勝率
    #若交易次數=0，則勝率=0
    if count == 0 :
        w = 0
    else :
        w = df['ret'][df['ret']>0].count() / count 
    #將最後報酬、交易次數、最大回檔、勝率，統整成表格
    result = pd.DataFrame({
        '最後報酬':[last],
        '總賺錢點數':[wamt],
        '總賠錢點數':[lamt],
        '交易次數':[count],
        '最大回檔':[mdd],
        '勝率':[w]
    })

    return(result)

#輸出回測結果到Excel 檔案
#mane為指定輸出excel檔案名稱，df為輸出資料內容，result 為績效指標
#k為保留k線數，L為總資料筆數
def out_excle(name,df,result,K,L) :
    writer = pd.ExcelWriter('/Users/Tony/Downloads/'+ name+'.xlsx',engine=None)
    df.to_excel(writer,'0') #將df資料輸出到 '0' 工作表
    result.to_excel(writer,'result') #將result資料輸出到 'result' 工作表
    #將df['cus']資料輸出到'result'工作表，指定第5欄輸出
    df['cus'].to_excel(writer,'result',startcol=5)
   
    writer.save()



# 讀取資料
df = pd.read_csv('/Users/Tony/Downloads/abc_22.csv',encoding="UTF8")

MA(5,10,df)
RSI(6,df)
BoxTheory(df,5)


#進行買賣
K = 10 #設定保留K線參數
L = len(df) #取得筆數
r=0 #記錄交易資金流量
b=0 #設定多空方，多方=1，空方=-1，空手=0
df['sign']=0 #新增欄位，用來記錄進場多空
df['ret']=0 #新增欄位，用來記錄出勤結算
df['note']='' #記錄交易指數

#由於序號從0開始，迴圈從第k-1筆記錄開始執行
for i in range(K-1,L):
 
    #若 i < 最後一筆，則執行
    if i < L-1 :
        #若 b = 1 ,表示多
        if b == 1 :
            #若死亡交叉，則以下一筆開盤價執行多方出場
            if df['box_sign'].iloc[i] == -1  : # or df['ma_sign'].iloc[i] == -1  : # or df['rsi_sign'].iloc[i] == -1 :
                (r,b) = outp(df,r,b,1,i+1)
            else :#停利、停損
                  (r,b)=stop(df,200,-50,r,b,i)
        
        elif b == -1 :
            #黃金交叉，則以下一筆開盤價執行多方出場
            if  df['box_sign'].iloc[i] == 1  : #  or df['ma_sign'].iloc[i] ==  1  : # or df['rsi_sign'].iloc[i] == 1 :
                (r,b) = outp(df,r,b,1,i+1)
            else :#停利、停損
                (r,b)=stop(df,200,-50,r,b,i)
         
            #若b=0,表示空手
        elif b == 0 :
                #若黃金交叉，則以下一筆開盤價執行多方進場
            if  df['box_sign'].iloc[i] == 1 : # df['ma_sign'].iloc[i] == 1 :# or df['rsi_sign'].iloc[i] == 1 :
                r,b = inp(df,r,1,i+1)
            elif  df['box_sign'].iloc[i] == -1 : #  df['ma_sign'].iloc[i] == -1 : # or df['rsi_sign'].iloc[i] == -1 :
                r,b = inp(df,r,-1,i+1)   
               
    elif i == L-1 :
        #若b不等於0 (表示還有部位)
        if b != 0 :
            (r,b) = outp(df,r,b,4,i)

#計算累計損益
df['cus'] = df['ret'].cumsum()
#df['cus'].plot()#繪圖
#計算各項策略績效指標
result = result_F(df)
out_excle('st1',df,result,K,L)





#pd.set_option('display.max_rows', df.shape[0]+1)
#print(df)