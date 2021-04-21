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
# 定義威廉指標的週期、超買區、超賣區
WILLRPeriod=14
OverBuy = -20
OverSell = -80

# 假設只有多單進場，本進場條件毫無意義，僅供測試
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price=float(i[2])
    Index=1
    OrderTime=time
    OrderPrice=price
    print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
    GO.EndDescribe()

# 出場判斷
if Index==1:
    # 多單出場判斷
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        tag=KBar.TimeAdd(time,price,qty) 
        
        # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
        if tag != 1:
            continue
            
        Real = KBar.GetWILLR(WILLRPeriod)
        # 當威廉指標已經計算完成，才會去進行判斷
        if len(Real) > WILLRPeriod +1:
            ThisReal = Real[-1-tag]
            LastReal = Real[-2-tag]
            # 進入超買區
            if LastReal >= OverBuy and ThisReal < OverBuy:
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
elif Index==-1:
    # 空單出場判斷
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        tag=KBar.TimeAdd(time,price,qty) 
        
        # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
        if tag != 1:
            continue
            
        Real = KBar.GetWILLR(WILLRPeriod)
        # 當威廉指標已經計算完成，才會去進行判斷
        if len(Real) > WILLRPeriod +1:
            ThisReal = Real[-1-tag]
            LastReal = Real[-2-tag]
            # 進入超賣區
            if LastReal >= OverSell and ThisReal < OverSell:
                Index=0
                CoverTime=time
                CoverPrice=price            
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                GO.EndDescribe()