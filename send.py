import http.client
from receive import token 
conn = http.client.HTTPSConnection("api.shisanshui.rtxux.xyz")


import cal
userid,card=cal.main()

payload = "{\"id\"%s,\"card\":[\"%s %s %s\",\"%s %s %s %s %s\",\"%s %s %s %s %s\"]}"%(userid,card[0],card[1],card[2],
                                                                                             card[3],card[4],card[5],card[6],card[7],
                                                                                    card[8],card[9],card[10],card[11],card[12])

headers = {
    'content-type': "application/json",
    'x-auth-token': token
    }

conn.request("POST", "/game/submit", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
