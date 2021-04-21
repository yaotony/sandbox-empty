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
# 定義量能平均週期
VolumePeriod = 10

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

    QMA = KBar.GetQMA(VolumePeriod)
    # 當慢線已經計算完成，才會去進行判斷
    if len(QMA) > VolumePeriod+1:
        # 當前分鐘成交量
        ThisQ=KBar.GetVolume()[-1-tag]
        # 之前平均的量平均
        LastAvgQ=QMA[-2-tag]

        # 當目前成交量突破 前N分鐘的平均值 定義為爆量進場
        if ThisQ > LastAvgQ:
            Close=KBar.GetClose()[-1-tag]
            Open=KBar.GetOpen()[-1-tag]
            # 如果爆量的當下 收盤價大於開盤價則做多
            if Close > Open :
                Index=1
                OrderTime=time
                OrderPrice=price            
                print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
                GO.EndDescribe()
            # 如果爆量的當下 收盤價大於開盤價則做空
            elif Close < Open:
                Index=-1
                OrderTime=time
                OrderPrice=price            
                print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
                GO.EndDescribe()
