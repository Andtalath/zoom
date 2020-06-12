import http.client
import json, csv
import sys
import jwt
from datetime import datetime
from datetime import timedelta
#import time
sys.path.append('../')
import secret

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.now() + timedelta(minutes=15)
}

jwt_encoded = str(jwt.encode(payload, secret.api_sec))
psw = jwt_encoded[2:-1]

try:
	from_date = sys.argv[1]
except:
	from_date = input("From date, ex 2019-05-01: ")
else:
	from_date = sys.argv[1]

try:
	to_date = sys.argv[2]
except:
	to_date = input("To Date, ex 2019-05-31: ")
else:
	to_date = sys.argv[2]

csv_file_path = "statistics-" + from_date + "-" + to_date + ".csv"

conn = http.client.HTTPSConnection("eu01web.zoom.us")
headers = { 'authorization': "Bearer "+psw }

with open(csv_file_path, mode='w') as meeting_file:
    meeting_writer = csv.writer(meeting_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    meeting_writer.writerow(["meeting_id", "email", "host", "topic", "start_time", "end_time", "duration", "participants", "user_type"])
          
    conn.request("GET", "/v2/metrics/meetings?type=past&from="+from_date+"&to="+to_date+"&page_size=300", headers=headers)
    res = conn.getresponse()
    data = res.read()
    raw_data = json.loads(data)
    
    try:
        next_page_token = (raw_data['next_page_token'])
    except:
        next_page_token = ""
    else:
        next_page_token = (raw_data['next_page_token'])
    
    for meeting in raw_data['meetings']:
        mid = (meeting['id'])
        email = (meeting['email'])
        host = (meeting['host'])
        topic = (meeting['topic'])
        start_time = datetime.strptime((meeting['start_time']), '%Y-%m-%dT%H:%M:%SZ')
        st_text = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime((meeting['end_time']), '%Y-%m-%dT%H:%M:%SZ')
        et_text = end_time.strftime("%Y-%m-%d %H:%M:%S")
        duration = (meeting['duration'])
        if len(duration) <6:
            duration = "00:" + duration
        participants = (meeting['participants'])
        user_type = (meeting['user_type'])
        
        meeting_writer.writerow([mid, email, host, topic, st_text, et_text, duration, participants, user_type])

    while next_page_token != "":
        #time.sleep(0.5)
        print(next_page_token)
        conn.request("GET", "/v2/metrics/meetings?type=past&from="+from_date+"&to="+to_date+"&page_size=300&next_page_token="+next_page_token, headers=headers)
        res = conn.getresponse()
        data = res.read()
        raw_data = json.loads(data)
        #print(raw_data)
        try:
            next_page_token = (raw_data['next_page_token'])
        except:
            next_page_token = ""
        else:
            next_page_token = (raw_data['next_page_token'])
            
        for meeting in raw_data['meetings']:
            mid = (meeting['id'])
            email = (meeting['email'])
            host = (meeting['host'])
            topic = (meeting['topic'])
            start_time = datetime.strptime((meeting['start_time']), '%Y-%m-%dT%H:%M:%SZ')
            st_text = start_time.strftime("%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime((meeting['end_time']), '%Y-%m-%dT%H:%M:%SZ')
            et_text = end_time.strftime("%Y-%m-%d %H:%M:%S")
            duration = (meeting['duration'])
            if len(duration) <6:
                duration = "00:" + duration
            participants = (meeting['participants'])
            user_type = (meeting['user_type'])

            meeting_writer.writerow([mid, email, host, topic, st_text, et_text, duration, participants, user_type])
