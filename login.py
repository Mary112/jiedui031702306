
import http.client

conn = http.client.HTTPSConnection("api.shisanshui.rtxux.xyz")
username="hhhhhwwww"
password="abcde"
payload = "{\"username\":\"%s\",\"password\":\"%s\"}"%(username,password)

headers = { 'content-type': "application/json" }

conn.request("POST", "/auth/login", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
"""user_id:400"""
