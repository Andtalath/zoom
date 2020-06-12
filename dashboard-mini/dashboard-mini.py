import http.client
import json
import jwt
import datetime
from datetime import timedelta
sys.path.append('../')
import secret

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.datetime.now() + datetime.timedelta(minutes=5)
}

jwt_encoded = str(jwt.encode(payload, secret.api_sec))
jwt_encoded = jwt_encoded[2:]
jwt_encoded = jwt_encoded[:-1]

conn = http.client.HTTPSConnection("api.zoom.us")

headers = { 'authorization': "Bearer "+jwt_encoded }

with open('zoom-dashboard-mini.html', 'w') as f:
    f.write("<h2>Zoom Dashboard mini</h2>\n")

    conn.request("GET", "/v2/metrics/meetings?type=live", headers=headers)
    res = conn.getresponse()
    data = res.read()
    jdata = json.loads(data)
    ameetings = str(jdata['total_records'])

    conn.request("GET", "/v2/metrics/webinars?type=live", headers=headers)
    res = conn.getresponse()
    data = res.read()
    jdata = json.loads(data)
    awebinars = str(jdata['total_records'])

    f.write("<b>Live In Progress:</b> "+ameetings+ " Meetings & "+awebinars+" Webinars<br>\n")

    conn.request("GET", "/v2/users?status=active", headers=headers)
    res = conn.getresponse()
    data = res.read()
    jdata = json.loads(data)
    users = str(jdata['total_records'])

    from_date = str(datetime.datetime.now().date() - timedelta(days=7))
    conn.request("GET", "/v2/report/users?from="+from_date+"&type=active", headers=headers)
    res = conn.getresponse()
    data = res.read()
    jdata = json.loads(data)

    tusers = str(jdata['total_records'])
    tmeetings = str(jdata['total_meetings'])
    tparticipants = str('{:,}'.format(jdata['total_participants']).replace(',', '.'))
    tminutes = str('{:,}'.format(jdata['total_meeting_minutes']).replace(',', '.'))

    f.write("<b>Last 7 days:</b> "+tusers+"(of "+users+") Active Users and "+tmeetings +" Meetings with total "+tparticipants+" participants and "+tminutes+" Meeting Minutes<br>")
