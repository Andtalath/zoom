import http.client
import json
import jwt
import datetime
from datetime import timedelta
from datetime import datetime
import secret

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.now() + timedelta(minutes=5)
}

jwt_encoded = str(jwt.encode(payload, secret.api_sec))
jwt_encoded = jwt_encoded[2:]
jwt_encoded = jwt_encoded[:-1]

conn = http.client.HTTPSConnection("eu01web.zoom.us")

headers = { 'authorization': "Bearer "+jwt_encoded }

conn.request("GET", "/v2/roles", headers=headers)
res = conn.getresponse()
data = res.read()
jdata = json.loads(data)

print("Creating role-memebers.txt ...")

open('role-members.txt', 'w').close()

for roles in jdata['roles']:
    id = roles['id']
    description = roles['description']
    if id != "2":
        conn.request("GET", "/v2/roles/"+id+"/members", headers=headers)
        res = conn.getresponse()
        mdata = res.read()
        jmdata = json.loads(mdata)
        total = str(jmdata['total_records'])
        email = ''
        for members in jmdata['members']:
            email = email + (members['email']) + "; "
        email = email[:-2]
        with open('role-members.txt', 'a') as f:
            f.write(description+", total records: "+total+"\n")
            f.write(email+"\n")
