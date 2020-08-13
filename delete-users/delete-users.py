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