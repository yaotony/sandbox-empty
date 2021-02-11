
def OBVTheory(df,s,l):
#平均線產生
    df['obv_Volume'] = 0
    obv_Volume = 0
    for i in  range( len(df)):
        if i == 0 :
            df['obv_Volume'].iloc[i] = df['Volume'].iloc[i]
            obv_Volume = df['Volume'].iloc[i]
        else :
            if df['Close'].iloc[i] > df['Close'].iloc[i-1] :
                obv_Volume = obv_Volume + df['Volume'].iloc[i]
                df['obv_Volume'].iloc[i] = obv_Volume 
            elif df['Close'].iloc[i] < df['Close'].iloc[i-1] :
                obv_Volume = obv_Volume - df['Volume'].iloc[i]
                df['obv_Volume'].iloc[i] = obv_Volume
            else :
                df['obv_Volume'].iloc[i] = obv_Volume


    df['obv_s'] = df['obv_Volume'].iloc[:].rolling(s).mean()#以收盤價[close]計算5日均線 
    df['obv_l'] = df['obv_Volume'].iloc[:].rolling(l).mean()#以收盤價[close]計算10日均線 
    #MA 交易訊號欄
    df['obv_sign']=0
    #設定黃金交叉訊號
     #df['obv_sign'][(df['obv_s'].shift(1) < df['obv_l'].shift(1)) & (df['obv_s'] > df['obv_l']) ]=1
    #設定死亡交叉訊號
     #df['obv_sign'][(df['obv_s'].shift(1) > df['obv_l'].shift(1)) & (df['obv_s'] < df['obv_l']) ]=-1
    for i in  range( len(df)) :
        if (df['obv_s'].iloc[i-1]  <  df['obv_l'].iloc[i-1] ) & (df['obv_s'].iloc[i]  >  df['obv_l'].iloc[i] ) :
            df['obv_sign'].iloc[i] =1
        elif (df['obv_s'].iloc[i-1]  >   df['obv_l'].iloc[i-1] ) & (df['obv_s'].iloc[i]  <  df['obv_l'].iloc[i] ) :
            df['obv_sign'].iloc[i] =-1
   