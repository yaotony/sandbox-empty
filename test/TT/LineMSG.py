import lineTool
import requests

#token='BGMktHvxXppQctxavvBkKl3aNPjKgG027mWIF4z9a46'
token='vkI9hP7Ildv4HkxY63nWV6CTFjk45yGMgpnw6eJk88u'


URL = 'https://notify-api.line.me/api/notify'
  
  
def send_message( msg, img=None):
    """Send a LINE Notify message (with or without an image)."""
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message': msg}
    files = {'imageFile': open(img, 'rb')} if img else None
    r = requests.post(URL, headers=headers, params=payload, files=files)
    if files:
        files['imageFile'].close()
    return r.status_code

#r = send_message('ABC','c:\\temp\\20200106121100.png')
#print(r)
#send_message('AAGC')
