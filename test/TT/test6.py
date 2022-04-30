from numpy import dsplit
from Log import add,logFileClear,readCsvLog
import time ,datetime
import pandas as pd



orderFileName =datetime.datetime.now().strftime('%Y%m%d')+'_order'
df  =  readCsvLog(orderFileName)
#print(df)

for i in  range( len(df)):
    timeValue=  df.iloc[i][0]
    Price =  df.iloc[i][1]
    BS =  df.iloc[i][2]
    print('BS:',BS,' Price:',Price,' Time:',timeValue)


print('-----BS:',df.iloc[-1][2],' Price:',df.iloc[-1][1],' Time:',df.iloc[-1][0])

