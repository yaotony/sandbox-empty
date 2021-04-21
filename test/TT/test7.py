import os
import subprocess

command =r"E:\FubonAPIDemoF\(C#)FubonAPIDemo\FubonAPIDemoPro\bin\Debug\FubonAPIDemoPro.exe"

#subprocess.call([command, 'quity'])
res = os.popen("\"E:\\FubonAPIDemoF\\(C#)FubonAPIDemo\\FubonAPIDemoPro\\bin\\Debug\\FubonAPIDemoPro.exe\" view 10 DwqeqEF")
ls = res.readlines()
print (int( ls[0]))
print (ls[1])
#os.Popen(command)
#res = subprocess.Popen([command, 'view'])

#print(res)

