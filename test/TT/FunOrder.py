import os

command = "\"E:\\FubonAPIDemoF\\(C#)FubonAPIDemo\\FubonAPIDemoPro\\bin\\Debug\\FubonAPIDemoPro.exe\" "
#command = "\"D:\\FRun\\FubonAPIDemoPro.exe\" "

def efOrder(yymm,bs,qty):
    res = os.popen( f"{command} order {yymm} {bs} {qty}")
    
    price = res.read().replace('Active code page: 52936','').replace('\n','')
    print(f'efOrder: {price} ,{yymm} ,{bs}, {qty}')
    return  int(price)

def getPositionQty():
    res = os.popen(f"{command} viewQty ")
    
    qty = res.read().replace('Active code page: 52936','').replace('\n','')
    print(f'getPositionQty: {qty} ')
    return  int(qty)
    
def getPositionBS():
    res = os.popen(f"{command} viewBS ")
    bs = res.read().replace('Active code page: 52936','').replace('\n','')

    return  bs


def getQuity():
    res = os.popen(f"{command} quity ")
    quity = res.read().replace('Active code page: 52936','').replace('\n','')

    return  quity


def getMatch():
    res = os.popen(f"{command} match ")
    r = res.read().replace('Active code page: 52936','')

    return  r

#r = efOrder('202105','S','1')
#print(r)

print('Qty：',getPositionQty())
print('BS：',getPositionBS())
print('Quity',getQuity())
print(getMatch())

