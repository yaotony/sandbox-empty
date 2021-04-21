import haohaninfo
GOC = haohaninfo.GOrder.GOCommand()
GOQ = haohaninfo.GOrder.GOQuote()

# 市價委託單(預設非當沖、倉別自動)
def OrderMKT(Broker,Product,BS,Qty,DayTrade='0',OrderType='A'):
    # 送出交易委託
    # print([Broker, Product, BS, '',str(Qty), "IOC", "MKT" ,str(DayTrade),OrderType])
    OrderNo=GOC.Order(Broker, Product, BS, '0',str(Qty), "IOC", "MKT" ,str(DayTrade),OrderType)
    # print(OrderNo)
    # 判斷是否委託成功(這邊以元富為例)
    if OrderNo != '委託失敗':
        while True:
            # 取得成交帳務
            MatchInfo=GOC.MatchAccount(Broker,OrderNo)
            # 判斷是否成交
            if MatchInfo != []:
                # 成交則回傳
                return MatchInfo[0].split(',')
    else:
        return False
            
import time

# 限價委託單到期刪單(預設非當沖、倉別自動、N秒尚未成交刪單[預設10])
def OrderLMT(Broker,Product,BS,Price,Qty,DayTrade='0',OrderType='A',Wait=10):
    # 送出交易委託
    OrderNo=GOC.Order(Broker,Product,BS,str(Price),str(Qty),"ROD","LMT",str(DayTrade),OrderType)
    # 設定刪單時間
    EndTime=time.time()+Wait
    # 判斷是否委託成功(這邊以元富為例)
    if OrderNo != '委託失敗':
        # 若大於刪單時間則跳出迴圈
        while time.time() < EndTime:
            # 取得成交帳務
            MatchInfo=GOC.MatchAccount(Broker,OrderNo)
            # 判斷是否成交
            if MatchInfo != []:
                # 成交則回傳
                return MatchInfo[0].split(',')
            # 稍等0.5秒
            time.sleep(0.5)
            print(OrderNo,'尚未成交')
        # 刪單並確認委託成功刪除
        GOC.Delete(Broker,OrderNo)
        GOC.GetAccount(Broker,OrderNo)
        print('到期刪單')
        return False
    else:
        return False            
            
# 範圍市價單(預設非當沖、倉別自動、掛上下N檔價1-5[預設3]、N秒尚未成交刪單[預設10])
def OrderRangeMKT(Broker,Product,BS, Qty,DayTrade='0',OrderType='A',OrderPriceLevel=3,Wait=10): 
    # 新增訂閱要下單的商品，預防沒有取到該商品報價
    GOC.AddQuote(Broker,Product,True)
    # 取得委託商品的上下五檔來進行限價委託(這邊預設下單與報價使用同一個券商，若不同則需另外調整)
    UpdnInfo=GOQ.SubscribeLast(Broker,'updn5',Product)
    # 如果是買單，則掛上五檔委託
    if BS == 'B':
        OrderPoint=UpdnInfo[OrderPriceLevel*2]
    elif BS == 'S':
        OrderPoint=UpdnInfo[10+OrderPriceLevel*2]
    # 送出交易委託
    print([Broker, Product, BS, str(OrderPoint), str(Qty), "ROD", "LMT" ,str(DayTrade),OrderType])
    OrderNo=GOC.Order(Broker, Product, BS, str(OrderPoint), str(Qty), "ROD", "LMT" ,str(DayTrade),OrderType )
    # 設定刪單時間
    EndTime=time.time()+Wait
    # 判斷是否委託成功(這邊以元富為例)
    if OrderNo != '委託失敗':
        # 若大於刪單時間則跳出迴圈
        while time.time() < EndTime:
            # 取得成交帳務
            MatchInfo=GOC.MatchAccount(Broker,OrderNo)
            # 判斷是否成交
            if MatchInfo != []:
                # 成交則回傳
                return MatchInfo[0].split(',')
            # 稍等0.5秒
            time.sleep(0.5)
            print('尚未成交')
        # 刪單並確認委託成功刪除
        GOC.Delete(Broker,OrderNo)
        GOC.GetAccount(Broker,OrderNo)
        print('到期刪單')
        return False
    else:
        return False 

# 範圍市價單(預設非當沖、倉別自動、掛上下N檔價1-5[預設3]、N秒尚未成交刪單[預設10])
def RangeMKTDeal(Broker,Product,BS, Qty,DayTrade='0',OrderType='A',OrderPriceLevel=3,Wait=10):
    # 防止例外狀況，最多下三次單
    for i in range(3):
        OrderInfo=OrderRangeMKT(Broker,Product,BS,Qty,DayTrade,OrderType,OrderPriceLevel,Wait)
        if OrderInfo != False:
            return OrderInfo
    # 三次委託皆失敗，建議當日不做交易
    return False

# 透過期貨價格轉換選擇權特定履約價商品
def FutureToOption(Broker,FProduct,OptionContract,CallPut,ExcuteGap,OutInLevel): 
    # 取得委託商品的上下五檔來進行限價委託(這邊預設下單與報價使用同一個券商，若不同則需另外調整)
    MatchInfo=GOQ.SubscribeLast(Broker,'match',FProduct)
    MatchPrice=float(MatchInfo[2])
    print('期貨當前價:',MatchPrice)
    # 取得價平履約價(如果剛好在履約價間距中間，則往上加履約價)
    if MatchPrice%ExcuteGap>=ExcuteGap/2 :
        ExcutePrice=MatchPrice-(MatchPrice%ExcuteGap)+ExcuteGap
    else:
        ExcutePrice=MatchPrice-(MatchPrice%ExcuteGap)
    # 判斷買權賣權、計算履約價
    if CallPut.lower() == 'call':
        ExcutePrice-=ExcuteGap*OutInLevel
        print('計算履約價:',ExcutePrice)
        return OptionContract+str(int(ExcutePrice))+FProduct[-2:]
    elif CallPut.lower() == 'put':
        ExcutePrice+=ExcuteGap*OutInLevel
        print('計算履約價:',ExcutePrice)
        return OptionContract+str(int(ExcutePrice))+FProduct[-2:]

#◆ 券商代碼，如：Simulator。
Broker='Simulator'
#◆ 商品名稱，如：TXFF9、MXFE9。
Product ='MXFD1' 
#◆ 下單方向，如：B（多單）、S（空單）。
BS ='S' 
#◆ 下單價位，如：10000、10010、10020。
Price =  0 
#◆ 下單口數，如：1、2、3。
Qty= 1 
#◆ 是否當沖，如：1（當沖）、0（非當沖）
DayTrade = 1

#MatchInfo = OrderMKT(Broker,Product,BS,Qty,DayTrade,'A')
#print('OrderMKT',MatchInfo)
MatchInfo = OrderRangeMKT(Broker,Product,BS,Qty,DayTrade)

print('OrderRangeMKT',MatchInfo)
print('成交價:',MatchInfo[4])


vv = GOC.GetInStock(Broker,'All')
print(vv)


#◆ 時間類別，如：ROD（當日委託有效）、IOC（立即成交否則取消）、FOK（全部成交否則取消）。
#◆ 價格類別，如：LMT（限價單）、MKT（市價單）。










