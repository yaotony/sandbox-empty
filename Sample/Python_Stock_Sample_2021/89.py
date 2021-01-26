# 載入相關套件
import haohaninfo,indicator,datetime,time,sys

# 選擇報價平台
Broker = sys.argv[1]
# 定義商品名稱
Prod = sys.argv[2]

OutDeskAmount=0
InDeskAmount=0

# 訂閱報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 定義成交價、成交量、買價、賣價
    Price=float(row[2])
    Qty=int(row[3])
    DnPrice=float(row[5])
    UpPrice=float(row[6])
    # 內外盤判斷
    if Price >= UpPrice:
        OutDeskAmount += Qty
        print(Time,'外盤成交 總量:',OutDeskAmount)
    elif Price <= DnPrice:
        InDeskAmount += Qty
        print(Time,'內盤成交 總量:',InDeskAmount)