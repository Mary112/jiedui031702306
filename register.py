
import http.client

conn = http.client.HTTPSConnection("api.shisanshui.rtxux.xyz")

payload = "{\"username\":\"hhhhhwwww\",\"password\":\"abcde\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/auth/register", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
"""*9 #2 &10 #A $6 &6 #3 #Q #4 $4 *3 $8 *6"""
