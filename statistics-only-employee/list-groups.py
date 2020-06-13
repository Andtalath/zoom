import http.client
import sys
import json
import jwt
from datetime import datetime
from datetime import timedelta
sys.path.append('../')
import secret

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.now() + timedelta(minutes=15)
}

jwt_encoded = str(jwt.encode(payload, secret.api_sec))
psw = jwt_encoded[2:-1]

conn = http.client.HTTPSConnection("api.zoom.us")
headers = { 'authorization': "Bearer "+psw }

conn.request("GET", "/v2/groups", headers=headers)

res = conn.getresponse()
data = res.read()
raw_data = json.loads(data)

print (raw_data)
