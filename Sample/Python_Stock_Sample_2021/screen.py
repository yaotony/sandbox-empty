# 載入套件
import requests,json,datetime
from bs4 import BeautifulSoup
import numpy as np

# 取得股票定價交易資訊
def GetStockAfterHour(date,selectType):
    # 取得網站內容
    html= requests.get('https://www.twse.com.tw/exchangeReport/BFT41U?response=json&date='+date+'&selectType='+selectType)

    #成功取得網頁
    if html.status_code == requests.codes.ok:
        jcontent=json.loads(html.text)
        data=jcontent['data']
        data1=[ [ j.replace(',','') for j in i ] for i in data if i[1]!= '合計' ]
        return data1
    else:
        print('爬蟲失敗')
        return False

# 取得股票融資融券資訊
def GetMarginTrade(date,selectType):
    # 取得網站內容
    html= requests.get('https://www.twse.com.tw/exchangeReport/MI_MARGN?response=json&date='+date+'&selectType='+selectType)

    #成功取得網頁
    if html.status_code == requests.codes.ok:
        jcontent=json.loads(html.text)
        data=jcontent['data']
        data1=[ [ j.replace(',','') for j in i ] for i in data if i[1]!= '合計' ]
        return data1
    else:
        print('爬蟲失敗')
        return False
        
# 取得股票融券借券資訊
def GetCraditTrade(date):
    # 取得網站內容
    html= requests.get('https://www.twse.com.tw/exchangeReport/TWT93U?response=json&date='+date)

    #成功取得網頁
    if html.status_code == requests.codes.ok:
        jcontent=json.loads(html.text)
        data=jcontent['data']
        data1=[ [ j.replace(',','') for j in i ] for i in data if i[1]!= '合計' ]
        return data1
        return data
    else:
        print('爬蟲失敗')
        return False
        
# 取得三大法人彙總資訊(type參數分別是1外資,2自營商,3投信)
def GetThreeMajor(date,type=1):       
    if type== 1: 
        # 外資彙總表
        URL='https://www.twse.com.tw/fund/TWT38U?response=json&date='+date
    elif type == 2:
        # 自營商彙總表網址
        URL='https://www.twse.com.tw/fund/TWT43U?response=json&date='+date
    elif type == 3:
        # 投信彙總表網址
        URL='https://www.twse.com.tw/fund/TWT44U?response=json&date='+date
    else:
        return False
    
    # 取得網站內容
    html= requests.get(URL)

    #成功取得網頁
    if html.status_code == requests.codes.ok:
        jcontent=json.loads(html.text)
        data=jcontent['data']
        data1=[ [ j.replace(',','') for j in i ] for i in data ]
        return data1
    else:
        print('爬蟲失敗')
        return False
        
# 取得熱門排行榜資訊
def GetHotRank(t,e,n):       
    # 網址
    URL='https://tw.stock.yahoo.com/d/i/rank.php?t='+t+'&e='+e+'&n='+n

    # 取得網站內容
    html= requests.get(URL)

    #成功取得網頁
    if html.status_code == requests.codes.ok:
        # 透過 BeautifulSoup 解析該網站
        soup=BeautifulSoup(html.text,'html.parser')
        # 取得表格內資訊
        rs_list=[]
        for tr in soup.find_all('tr',bgcolor='#ffffff'):
            tr_content = [ i.text.replace(',','') for i in tr.find_all('td') ]
            rs_list.append(tr_content)
        return rs_list
    else:
        print('爬蟲失敗')
        return False

# 取得外資熱門排行榜資訊(type參數分別是1單日買超排行,2上週買超排行,3單日賣超排行,4上週賣超排行)
def GetForeignRank(type=1):
    type=int(type)
    if type == 1:
        # 單日買超排行
        URL='https://tw.stock.yahoo.com/d/i/fgbuy_tse.html' 
    elif type == 2:
        # 上週買超排行
        URL='https://tw.stock.yahoo.com/d/i/fgbuy_tse_w.html' 
    elif type == 3:
        # 單日賣超排行
        URL='https://tw.stock.yahoo.com/d/i/fgsell_tse.html' 
    elif type == 4:
        # 上週賣超排行
        URL='https://tw.stock.yahoo.com/d/i/fgsell_tse_w.html' 
    else:
        return False

    # 取得網站內容
    html= requests.get(URL)

    #成功取得網頁
    if html.status_code == requests.codes.ok:
        # 透過 BeautifulSoup 解析該網站
        soup=BeautifulSoup(html.text,'html.parser')
        # 取得表格內資訊
        rs_list=[]
        for tr in soup.find_all('tr',bgcolor='#FFFFFF'):
            tr_content = [ i.text.replace(',','') for i in tr.find_all('td') ]
            rs_list.append(tr_content)
        return rs_list
    else:
        print('爬蟲失敗')
        return False
  
# 取得自營商熱門排行榜資訊(type參數分別是1單日買超排行,2上週買超排行,3單日賣超排行,4上週賣超排行)
def GetDealerRank(type=1):  
    type=int(type)
    if type == 1:
        # 單日買超排行
        URL='https://tw.stock.yahoo.com/d/i/sebuy_tse.html'
    elif type == 2:
        # 上週買超排行
        URL='https://tw.stock.yahoo.com/d/i/sebuy_tse_w.html'
    elif type == 3:
        # 單日賣超排行
        URL='https://tw.stock.yahoo.com/d/i/sesell_tse.html'
    elif type == 4:
        # 上週賣超排行
        URL='https://tw.stock.yahoo.com/d/i/sesell_tse_w.html'

    # 取得網站內容
    html= requests.get(URL)

    #成功取得網頁
    if html.status_code == requests.codes.ok:
        # 透過 BeautifulSoup 解析該網站
        soup=BeautifulSoup(html.text,'html.parser')
        # 取得表格內資訊
        rs_list=[]
        for tr in soup.find_all('tr',bgcolor='#FFFFFF'):
            tr_content = [ i.text.replace(',','') for i in tr.find_all('td') ]
            rs_list.append(tr_content)
        return rs_list
    else:
        print('爬蟲失敗')
        return False
    
# 取得權值股資訊
def GetWeightedStock():  
    # 網址
    URL='https://www.taifex.com.tw/cht/9/futuresQADetail'

    # 取得網站內容
    html= requests.get(URL)

    #成功取得網頁
    if html.status_code == requests.codes.ok:
        # 透過 BeautifulSoup 解析該網站
        soup=BeautifulSoup(html.text,'html.parser')
        # 取得表格內資訊
        rs_list=[]
        for tr in soup.find_all('tr',bgcolor='#FFFFFF'):
            # 移除特殊符號
            tr_content = [ i.text.strip() for i in tr.find_all('td') ]
            # 取出前後兩個部分
            first_stock=tr_content[:4]
            second_stock=tr_content[4:8]
            # 新增至統一的List中
            rs_list.append(first_stock)
            rs_list.append(second_stock)
        rs_list = [ i for i in rs_list if i[0] != '' ]
        rs_list.sort(key=lambda x:int(x[0]))
        return rs_list
    else:
        print('爬蟲失敗')
        return False

# 將民國年日期轉換為西元年
def ConvertYearFormat(YearStr):
    tmpdate=YearStr.split('/')
    return ''.join([str(int(tmpdate[0])+1911),tmpdate[1],tmpdate[2]])
    
# 取得股票日K線
def GetStockDailyOHLC(date,stock_symbol):
    # 取得網站內容
    html= requests.get('https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+date+'&stockNo='+stock_symbol)
    #成功取得網頁
    if html.status_code == requests.codes.ok:
        jcontent=json.loads(html.text)
        if jcontent['stat'] == '很抱歉，沒有符合條件的資料!':
            return []
        else:
            data=jcontent['data']
            data1=[ [ j.replace(',','') for j in i ] for i in data ]
            data2=[ [ConvertYearFormat(i[0]),float(i[3]),float(i[4]),float(i[5]),float(i[6]),float(i[1])/1000] for i in data1 ]
            return data2
    else:
        print('爬蟲失敗')
        return False
        
# 取得N日股票日K線
def GetNumberStockDaily(num,stock_symbol):
    currentTime= datetime.datetime.now()
    rs=[]
    while len(rs) <= num:
        currentMonth=currentTime.strftime('%Y%m') 
        rs.extend(GetStockDailyOHLC(currentMonth+'01',stock_symbol))
        while currentTime.strftime('%Y%m') == currentMonth:
            currentTime -= datetime.timedelta(1)
    rs.sort()
    return rs
        
# 取得股票日K線技術指標格式
def GetTAStockDaily(num,stock_symbol):
    KBar=GetNumberStockDaily(num,stock_symbol)
    TAKBar={}
    TAKBar['time']=np.array([ datetime.datetime.strptime(i[0],'%Y%m%d') for i in KBar ])
    TAKBar['open']=np.array([ i[1] for i in KBar ])
    TAKBar['high']=np.array([ i[2] for i in KBar ])
    TAKBar['low']=np.array([ i[3] for i in KBar ])
    TAKBar['close']=np.array([ i[4] for i in KBar ])
    TAKBar['volume']=np.array([ i[5] for i in KBar ])
    return TAKBar

