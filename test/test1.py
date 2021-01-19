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
        df['ris_sign'] =0
    #設定RSI指標超賣訊號= 0 (部位買進)
        df['ris_sign'][(df['rsi']<20)]= 1
    #設定RSI指標超買訊號= -1 (部位買進)
        df['ris_sign'][(df['rsi']>80)]= -1


#定義進場函數，呼號範例為(r,b) = inp(df,r,b,i)
def inp(df,r,b,i):
    #r=成本 b=多空方設定 多方=1 空方=1
    df('sign').iloc[i] = b #進場時記錄多空
    r = r - b * df.iloc[i,1] #設定多方買進與空方賣出成本
    return (r,b)
#定義出場函數，呼號範例為(r,b) = outp(df,r,b,price,i)
def outp(df,r,b,price,i):
    #r是資金存量，b=多空方設定 多方=1 空方=1
    #price=1代表開盤價，price=4代表收盤價
    df('ret').iloc[i] = r #進場時記錄多空
    r=0#歸零
    b=0#多空方歸零
    return (r,b)

# 讀取資料
df = pd.read_csv('/Users/Tony/Downloads/TWII.csv',encoding="BIG5")

MA(5,10,df)
RSI(6,df)

pd.set_option('display.max_rows', df.shape[0]+1)
print(df)