import pymssql 
import pandas as pd
import datetime
import time
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

_server = 'ap.joumingt.net' 
_database = 'MoneyMore' 
_username = 'mm' 
_password = '0958778940' 

def getConnect():
    global connect, cursor
    print("Connecting to database using pyodbc...")
    connect = pymssql.connect(server = _server,user=_username,password=_password,database=_database)
    cursor = connect.cursor()
    print("Succesfully Connected to database using pyodbc!")
    


def getDBData(strDate,endDate):
    getConnect()
    stock = pd.read_sql("select left([date],10) as Date ,[date] as Time, [Open] ,High,Low,[Close]  from dbo.GetIndexNumberByMin(1 ,'FUSA!WTX&','','','125')  where [date] between '"+strDate.strftime("%Y-%m-%d %H:%M:%S")+"' and '"+endDate.strftime("%Y-%m-%d %H:%M:%S")+"' order by Date", con = connect) #使用connect指定的Mysql獲取資料
   
    cursor.close()
    connect.close()
    return stock

