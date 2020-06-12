import http.client
import json
import sys
import jwt
import datetime
from datetime import timedelta
import time
sys.path.append('../')
import secret

ll_test = datetime.datetime.now() - timedelta(days=100)

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

page_number = (raw_data['page_number'])
page_count = (raw_data['page_count'])

print("Page "+str(page_number)+" of "+str(page_count))
time.sleep(0.5)

with open('cleanup-license.txt', 'w') as f:
    text ="e-mail\tfirst name\tlast name\ttype\tlast login time\tstatus"
    #print(text)
    f.write(text+"\n")

with open('cleanup-license.txt', 'a') as f:
    for user in raw_data['users']:
        email = (user['email'])
        fname = (user['first_name'])
        lname = (user['last_name'])
        ztype = (user['type'])

        try:
            user['last_login_time']
        except:
            llt_text = "Never logged in"
            if ztype != 1:
                old = "Check Manually"
            else:
                old = "OK"
        else:
            llt = datetime.datetime.strptime((user['last_login_time']), '%Y-%m-%dT%H:%M:%SZ')
            llt_text = llt.strftime("%Y-%m-%d %H:%M:%S")
            if ztype != 1 and llt < ll_test:
                old = "Changed to Basic"
            else:
                old = "OK"
    
        if ztype == 1 :
            ytype = "Basic"
        if ztype == 2 :
            ytype = "Licensed"
        if ztype == 3 :
            ytype = "On-Prem"
            
        text = email+"\t"+fname+"\t"+lname+"\t"+ytype+"\t"+llt_text+"\t"+old
        #print(text)
        if old == "Changed to Basic" :
            #print(text)
            payload = json.dumps({'type': 1}, ensure_ascii=True)
            conn.request("PATCH", "/v2/users/"+email, payload, headers)
            res = conn.getresponse()
            data = res.read()
            f.write(text+"\n")


while page_number != page_count:

    page_number = page_number+1
    print("Page "+str(page_number)+" of "+str(page_count))
    
    conn.request("GET", "/v2/users?page_number="+str(page_number)+"&page_size=300", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    raw_data = json.loads(data)

    #print(raw_data)
    time.sleep(0.5)
    
    with open('cleanup-license.txt', 'a') as f:
        for user in raw_data['users']:
            email = (user['email'])
            fname = (user['first_name'])
            lname = (user['last_name'])
            ztype = (user['type'])
            
            try:
                user['last_login_time']
            except:
                llt_text = "Never logged in"
                if ztype != 1:
                    old = "Check Manually"
                else:
                    old = "OK"
            else:
                llt = datetime.datetime.strptime((user['last_login_time']), '%Y-%m-%dT%H:%M:%SZ')
                llt_text = llt.strftime("%Y-%m-%d %H:%M:%S")
                if ztype != 1 and llt < ll_test:
                    old = "Changed to Basic"
                else:
                    old = "OK"
            
            if ztype == 1 :
                ytype = "Basic"
            if ztype == 2 :
                ytype = "Licensed"
            if ztype == 3 :
                ytype = "On-Prem"
            
            text = email+"\t"+fname+"\t"+lname+"\t"+ytype+"\t"+llt_text+"\t"+old
            #print(text)
            if old == "Changed to Basic" :
                #print(text)
                payload = json.dumps({'type': 1}, ensure_ascii=True)
                conn.request("PATCH", "/v2/users/"+email, payload, headers)
                res = conn.getresponse()
                data = res.read()
                f.write(text+"\n")
