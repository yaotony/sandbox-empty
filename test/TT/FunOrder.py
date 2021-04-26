import os

command = "\"E:\\FubonAPIDemoF\\(C#)FubonAPIDemo\\FubonAPIDemoPro\\bin\\Debug\\FubonAPIDemoPro.exe\" "

def efOrder(yymm,bs,qty):
    res = os.popen( f"{command} order {yymm} {bs} {qty}")
    price = res.read().replace('\n','')

    return  int(price)

def getPositionQty():
    res = os.popen(f"{command} viewQty ")
    qty = res.read().replace('\n','')

    return  int(qty)
    
def getPositionBS():
    res = os.popen(f"{command} viewBS ")
    bs = res.read().replace('\n','')

    return  bs


def getQuity():
    res = os.popen(f"{command} quity ")
    quity = res.read().replace(',','').replace('\n','')

    return  int(quity)


#r = efOrder('202105','S','1')
#print(r)

#print('Qty：'+str(getPositionQty()))
#print('BS：'+getPositionBS())