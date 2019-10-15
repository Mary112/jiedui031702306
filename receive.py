import http.client

from login import data
newdata = str(data,encoding="utf-8")
token=newdata.split("token\":\"")[1].split("\"")[0]
conn = http.client.HTTPSConnection("api.shisanshui.rtxux.xyz")

headers = { 'x-auth-token': token }

conn.request("POST", "/game/open", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
