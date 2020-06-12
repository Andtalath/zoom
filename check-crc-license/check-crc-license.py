import http.client
import json, csv
import sys
import jwt
from datetime import datetime
from datetime import timedelta
import secret

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.now() + timedelta(minutes=15)
}
jwt_encoded = str(jwt.encode(payload, secret.api_sec))
psw = jwt_encoded[2:-1]

conn = http.client.HTTPSConnection("eu01web.zoom.us")
headers = { 'authorization': "Bearer "+psw }

f = open("crc-date.csv")
csv_f = csv.reader(f)

print("Lista all occasions with more than 3 CRC license in use")

for row in csv_f:
	if not str(row[0]).startswith('#'):
		from_date = row[0]
		to_date = row[1]

		# Get CRC
		conn.request("GET", "/v2/metrics/crc?from="+from_date+"&to="+to_date, headers=headers)
		res = conn.getresponse()
		data = res.read()
		jdata = json.loads(data)
		#print(jdata)

		for x in jdata['crc_ports_usage']:
			day = (x['date_time'])
			for y in x['crc_ports_hour_usage']:
				if (y['max_usage']) > 3:
					hour = y['hour']
					usage = y['max_usage']
					text = str(day)+" "+str(hour)+":00, max usage="+str(usage)
					print(text)
