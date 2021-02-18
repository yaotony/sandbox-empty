import requests
import json
import pandas as pd

data = {
    "DateB": "2021/2/2 08:00:00",
    "DateE": "2021/2/2 14:00:00",
    "GroupCode": "FUSA!WTX&",
    "Key1": "",
    "Key2": "",
    "Key3": "125",
    "MinutesK": "1",
    "IsNoDataRefPre": True
}
url = "http://ap.joumingt.net:8858/moneymore/api/handleindexnumber.svc/GetIndexNumberOHLC"
data_json = json.dumps(data)
headers = {'Content-type': 'application/json'}
response = requests.post(url, data=data_json, headers=headers)
response_text = response.text
today_json = json.loads(response_text)
df = pd.json_normalize(today_json['d'])
print(df)