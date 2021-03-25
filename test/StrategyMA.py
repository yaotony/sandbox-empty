# MA策略 黃金交叉 = 1   死亡交叉 = -1  預設=0
def MA(s,l,df):
    #平均線產生
    df['ma_s'] = df['Open'].iloc[:].rolling(s).mean()#以收盤價[close]計算5日均線 
    df['ma_l'] = df['Open'].iloc[:].rolling(l).mean()#以收盤價[close]計算5日均線 
    #MA 交易訊號欄
    df['ma_sign']=0
    #設定黃金交叉訊號
    #df['ma_sign'][(df['ma_s'].shift(1) < df['ma_l'].shift(1)) & (df['ma_s'] > df['ma_l']) ]=1
    #設定死亡交叉訊號
    #df['ma_sign'][(df['ma_s'].shift(1) > df['ma_l'].shift(1)) & (df['ma_s'] < df['ma_l']) ]=-1
  
    for i in  range(len(df)) :
        if (df['ma_s'].iloc[i-1]  <  df['ma_l'].iloc[i-1] ) & (df['ma_s'].iloc[i]  >  df['ma_l'].iloc[i] ) :
            df['ma_sign'].iloc[i] =1
        elif (df['ma_s'].iloc[i-1]  >   df['ma_l'].iloc[i-1] ) & (df['ma_s'].iloc[i]  <  df['ma_l'].iloc[i] ) :
            df['ma_sign'].iloc[i] =-1
   