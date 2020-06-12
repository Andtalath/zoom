
import jwt
import datetime
import secret

# generate JWT
payload = {
'iss': secret.api_key,
'exp': datetime.datetime.now() + datetime.timedelta(minutes=5)
}

jwt_encoded = str(jwt.encode(payload, secret.api_sec))
jwt_encoded = jwt_encoded[2:-1]

print (jwt_encoded)