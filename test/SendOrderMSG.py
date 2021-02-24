import requests
import json
import pandas as pd

def sendMSG(msg,dataTime,IndexCalCode,ModellingSeconds) :
    url ="http://ap.joumingt.net:8858/moneymore/api/handleindexnumber.svc/SaveIndexCalNumber"
   #"BoxTheory"   Exit
    data = {
    "UserCode": "04", #不用動
    "IndexCalCode": IndexCalCode,  #不用動
    "Number": msg,  # 1=多點進  ,-1=空點進 
    "InsertDate": dataTime , #每一根k的時間
    "InsertMan": "Tony",
    "IsOrder":True,
    "ModellingSeconds": ModellingSeconds
    }

    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=data_json, headers=headers)
    response_text = response.text
    today_json = json.loads(response_text)
    return today_json
    #print(response)



