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
# 定義乖離率的週期、正乖離率臨界值、負乖離率臨界值
BIASPeriod=10
Positive=0.001
Negative=-0.001
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

    BIAS = KBar.GetBIAS(BIASPeriod)
    # 當乖離率已經計算完成，才會去進行判斷
    if len(BIAS) > BIASPeriod:
        BIAS = BIAS[-1-tag]

        # 超過負乖離率臨界值
        if Trend == 1 and BIAS <= Negative:
            Index=1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # 超過正乖離率臨界值
        elif Trend == -1 and BIAS >= Positive:
            Index=-1
            OrderTime=time
            OrderPrice=price            
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        


