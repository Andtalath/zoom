import http.client
import json
import sys
import jwt
import datetime
from datetime import timedelta
import time
from ldap3 import Server, Connection, ALL
import ldapinfo
sys.path.append('../')
import secret

# Connect to LDAP
server = Server(ldapinfo.server, get_info=ALL)
conn = Connection(server, ldapinfo.uid, ldapinfo.psw, auto_bind=True)

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.datetime.now() + datetime.timedelta(minutes=5)
}

jwt_encoded = str(jwt.encode(payload, secret.api_sec))
jwt_encoded = jwt_encoded[2:]
jwt_encoded = jwt_encoded[:-1]

conn = http.client.HTTPSConnection("api.zoom.us")

headers = {
    'content-type': "application/json",
    'authorization': "Bearer "+jwt_encoded
    }

conn.request("GET", "/v2/users?page_size=300", headers=headers)

res = conn.getresponse()
data = res.read()
raw_data = json.loads(data)