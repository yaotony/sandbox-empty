import requests
import json




url ="http://ap.joumingt.net:8858/moneymore/api/handleindexnumber.svc/SaveIndexCalNumber"
data = {
    "UserCode": "02", #不用動
    "IndexCalCode": "BoxTheory",  #不用動
    "Number": 1,  # 1=多點進  ,-1=空點進 , 3=出場
    "InsertDate": "2021/2/18 09:03:00", #每一根k的時間
    "InsertMan": "Ming"
}

data_json = json.dumps(data)
headers = {'Content-type': 'application/json'}
response = requests.post(url, data=data_json, headers=headers)
print(response)