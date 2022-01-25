import lineTool
import requests

AllSign='lMZV02Qhbhr2rLSz1hq0eijoJV08jDcZvQgeIDSsSZj'
BStoken='BGMktHvxXppQctxavvBkKl3aNPjKgG027mWIF4z9a46'
token='e5pRdh6BuC3LJ48Zk7OflU681BjuH1ziLdC2xPyxCv3'

#2022
newtoken ='9T4MggvtC2AFqN30shJ661zdxCnRO3Zb4HOEuUz4W9s'

URL = 'https://notify-api.line.me/api/notify'
  
def send_All_message( msg, img=None):
    """Send a LINE Notify message (with or without an image)."""
    headers = {'Authorization': 'Bearer ' + AllSign}
    payload = {'message': msg}
    files = {'imageFile': open(img, 'rb')} if img else None
    #r = requests.post(URL, headers=headers, params=payload, files=files)
    if files:
        files['imageFile'].close()
    #return r.status_code



def send_message( msg, img=None):
    """Send a LINE Notify message (with or without an image)."""
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message': msg}
    files = {'imageFile': open(img, 'rb')} if img else None
    r = requests.post(URL, headers=headers, params=payload, files=files)
    if files:
        files['imageFile'].close()
    return r.status_code


def send_bs_message( msg, img=None):
    """Send a LINE Notify message (with or without an image)."""
    headers = {'Authorization': 'Bearer ' + BStoken}
    payload = {'message': msg}
    files = {'imageFile': open(img, 'rb')} if img else None
    r = requests.post(URL, headers=headers, params=payload, files=files)
    if files:
        files['imageFile'].close()
    return r.status_code

#r = send_message('ABC','c:\\temp\\20200106121100.png')
#print(r)
#send_message('AAGC',None)
