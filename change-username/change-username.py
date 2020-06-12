import http.client
import json
import sys
import jwt
import datetime
from datetime import timedelta
import secret

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.datetime.now() + datetime.timedelta(minutes=15)
}

jwt_encoded = str(jwt.encode(payload, secret.api_sec))
psw = jwt_encoded[2:]
psw = psw[:-1]

# ask for usernames
try:
	user = sys.argv[1]
except:
	user = input("Username: ")
else:
	user = sys.argv[1]

try:
	new_id = sys.argv[2]
except:
	new_id = input("New username: ")
else:
	new_id = sys.argv[2]

print("\nIs this correct\nChange username =",user," to =",new_id)

def yes_or_no():
    YesNo = input("Yes or No?")
    YesNo = YesNo.lower()
    if(YesNo == "yes"):
        return 1
    elif(YesNo == "no"):
        return 0
    else:
        return yes_or_no()
        
answer = yes_or_no()
if answer == 1:
    print("Change username",user,"to",new_id,"...")
else:
    exit()

conn = http.client.HTTPSConnection("api.zoom.us")

headers = {
    'content-type': "application/json",
    'authorization': "Bearer "+psw
    }

# Change user name in Zoom
payload = "{\"email\":\"new_id\"}"
payload=payload.replace('new_id', new_id)

conn.request("PUT", "/v2/users/"+user+"/email", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
