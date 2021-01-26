import sys,requests,json

def getHistoryTick(broker,date,prod,table,path='C:/data/'):
    data_path=path+'/'+broker+'/'+date+'/'+prod+'_'+table+'.txt'
    data=open(data_path).readlines()
    rs=[ i.strip('\n').split(',') for i in data ]
    return rs
    
