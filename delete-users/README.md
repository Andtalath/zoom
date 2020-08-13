# EJ Klart!!!

# delete-users
Delete all users that are basic, last-login-time more then 365 days and don´t exists in LDAP.\
Results is in file delete-users.txt\
You also need rights to your LDAP.

### api url
* US = `api.zoom.us`
* EU = `eu01web.zoom.us`

## To run
* Install/Download python:
https://www.python.org/downloads/
* Install/Download pip
https://pip.pypa.io/en/stable/installing/
* Install deps:\
`pip install pyjwt`\
`pip install ldap3` more info at https://pypi.org/project/ldap3/
* Run the script:
`python .....`
