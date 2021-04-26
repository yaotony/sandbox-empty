import os
import subprocess
from Log import addLogTtxt

command =r"E:\FubonAPIDemoF\(C#)FubonAPIDemo\FubonAPIDemoPro\bin\Debug\FubonAPIDemoPro.exe"

#subprocess.call([command, 'quity'])
res = os.popen("\"E:\\FubonAPIDemoF\\(C#)FubonAPIDemo\\FubonAPIDemoPro\\bin\\Debug\\FubonAPIDemoPro.exe\" order 202105 S 1")
ls = res.readlines()
print (ls)
#print (ls[1])
addLogTtxt('eeeeeeeeeeeeeeee')
#os.Popen(command)
#res = subprocess.Popen([command, 'view'])

#print(res)
