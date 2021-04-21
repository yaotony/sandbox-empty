# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,indicator,datetime,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'match'
# 定義商品名稱
Prod = sys.argv[1]
# 取得當天日期
Date = datetime.datetime.now().strftime("%Y%m%d")
# K棒物件
KBar = indicator.KBar(Date,'time',1)
# 預設趨勢為1，假設只有多單進場
Trend=1

# 進場判斷
Index=0
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    tag=KBar.TimeAdd(time,price,qty) 
    
    # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
    if tag != 1:
        continue
        
    K,D = KBar.GetKD()
    # 當K值已經計算完成，才會去進行判斷
    if len(K) > 9+1:
        ThisK,LastK,ThisD,LastD = K[-1-tag],K[-2-tag],D[-1-tag],D[-2-tag]

        # 黃金交叉
        if Trend == 1 and LastK <= LastD and ThisK > ThisD:
            Index=1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # 死亡交叉
        elif Trend == -1 and LastK >= LastD and ThisK < ThisD:
            Index=-1
            OrderTime=time
            OrderPrice=price            
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        
