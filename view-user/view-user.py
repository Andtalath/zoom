import http.client
import json
import sys
import jwt
import datetime
from datetime import timedelta
import time
import secret

try:
	user = sys.argv[1]
except:
	user = input("ZOOM username, ex test@kth.se: ")
else:
	user = sys.argv[1]

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.datetime.now() + timedelta(minutes=5)
}

jwt_encoded = str(jwt.encode(payload, secret.api_sec))
jwt_encoded = jwt_encoded[2:]
jwt_encoded = jwt_encoded[:-1]

conn = http.client.HTTPSConnection("api.zoom.us")

headers = { 'authorization': "Bearer "+jwt_encoded }

# Get User info
conn.request("GET", "/v2/users/" + user, headers=headers)
res = conn.getresponse()
data = res.read()
jdata = json.loads(data)
#print(jdata)
pmi = (jdata['pmi'])
host_key = (jdata['host_key'])
first_name = (jdata['first_name'])
last_name = (jdata['last_name'])
ztype = (jdata['type'])
#print (jdata['group_ids'])
if ztype == 1 :
	ytype = "Basic"
if ztype == 2 :
	ytype = "Licensed"
if ztype == 3 :
	ytype = "On-Prem"
try:
	dept = (jdata['dept'])
except:
	dept = ""
else:
	dept = (jdata['dept'])
try:
	pmi_url = (jdata['vanity_url'])
except:
	pmi_url = ""
else:
	pmi_url = (jdata['vanity_url'])
try:
	last_login_time = (jdata['last_login_time'])
except:
	last_login_time = "Never logged in"
else:
	last_login_time = datetime.datetime.strptime((jdata['last_login_time']), '%Y-%m-%dT%H:%M:%SZ')

# Get pincode
conn.request("GET", "/v2/meetings/" + str(pmi), headers=headers)
res = conn.getresponse()
data = res.read()
jdata = json.loads(data)
try:
	pincode = (jdata['password'])
except:
	pincode = ""
else:
	pincode = (jdata['password'])

print("Personal Meeting ID =",pmi,"\nDepartment =",dept,"\nFirst & Last Name =",first_name,last_name,"\nHost Key =",host_key,"\nPin Code =",pincode)
print("Type = ",ytype)
print("Last login time = ",last_login_time)
print("Personal Link = ",pmi_url)

# Get assistants
conn.request("GET", "/v2/users/"+ user + "/assistants", headers=headers)
res = conn.getresponse()
data = res.read()
jdata = json.loads(data)

print ("Assistants =",[x["email"] for x in jdata["assistants"]])
