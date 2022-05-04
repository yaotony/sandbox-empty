from asyncio.windows_events import NULL
import csv
from lib2to3.pytree import convert
import time ,datetime
import pandas as pd
import os

def add(filename,note):
# 開啟輸出的 CSV 檔案
    with open('C:\\temp\\'+filename+'.csv', 'a', newline='', encoding='utf-8') as csvfile:
    # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)

        # 寫入一列資料
        writer.writerow(note)


def addLogTtxt(note):
    filename =datetime.datetime.now().strftime('%Y%m%d')
    with open('C:\\temp\\'+filename+'.txt', 'a', newline='', encoding='utf-8') as f:
        f.writelines(note+' \n')
        f.close

def logFileClear(filename):
    if os.path.exists('C:\\temp\\'+filename+'.csv'):
        os.remove('C:\\temp\\'+filename+'.csv')


def readCsvLog(filename):
    data = {}
    df = pd.DataFrame(data)
    if os.path.exists('C:\\temp\\'+filename+'.csv'):
        df =   pd.read_csv('C:\\temp\\'+filename+'.csv', header=None,dtype={1: int,2: int})
        
    return df
