# 載入相關套件
import haohaninfo,indicator,datetime,time,sys
from screen import GetNumberStockDaily

# 選擇報價平台
Broker = sys.argv[1]
# 定義商品名稱
Prod = sys.argv[2]

# 取得前一日收盤價資訊
LastDayInfo=GetNumberStockDaily(1,Prod)[-1]
LastClose=LastDayInfo[4]

print(LastDayInfo)

# 訂閱報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 定義成交價
    Price=float(row[2])
    # 判斷價格跳空(需要在開盤前就預先等待報價判斷開盤跳空判斷)
    if Price > LastClose:
        print(Time,'價格向上跳空',LastClose-Price)
    elif Price < LastClose:
        print(Time,'價格向下跳空',Price-LastClose)
    # 判斷完成以後跳出迴圈
    GO.EndSubscribe()

