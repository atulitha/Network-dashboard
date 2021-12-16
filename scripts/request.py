import requests
import json
url = 'https://prod-23.westus2.logic.azure.com:443/workflows/b900526b31d34127bcced445f5236024/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=wWNEhnN7BtQTEmpDQTX-vBssozLkqDPnX13PkPl8dhQ'


payload = "Syslog\r\n| where TimeGenerated >= ago(1m)\r\n| render table"
headers = {
  'Content-Type': 'text/plain'
}

r = requests.request("POST", url, headers=headers, data=payload)

t = r.text
j = json.load(r.text)
#print(t)
print(j)

#open('google.jpg', 'wb').write(r.content)