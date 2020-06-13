import http.client
import json
import jwt
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

conn.request("GET", "/v2/groups/"+groupid.groupId+"/members?page_number=1&page_size=300", headers=headers)

res = conn.getresponse()
data = res.read()
raw_data = json.loads(data)

page_number = (raw_data['page_number'])
page_count = (raw_data['page_count'])

print(page_number)
print(page_count)

employee=([x["email"] for x in raw_data["members"]])

with open('employee.txt', 'w') as f:
    for item in employee:
        f.write("%s\n" % item)

while page_number != page_count:

    print(page_number+1)
    page_number = page_number+1
    
    conn.request("GET", "/v2/groups/"+groupid.groupId+"/members?page_number="+str(page_number)+"&page_size=300", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    raw_data = json.loads(data)
    
    employee=([x["email"] for x in raw_data["members"]])
    
    with open('employee.txt', 'a') as f:
        for item in employee:
            f.write("%s\n" % item)
