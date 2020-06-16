# zoom-statistics-only-employee
Get statistics from Zoom and separates Student and Staff.\
Results is in files, ex: *statistics-2020-01-01-2020-01-31.csv, statistics-2020-01-01-2020-01-31-only-employee.csv & employee.txt*\
Edit groupid.py and add your groupId for employees only.
>You can specify a monthly date range for the dashboard data using the from and to query parameters. The month should fall within the last six months, see more at https://marketplace.zoom.us/docs/api-reference/zoom-api/dashboards/dashboardmeetings

### api url
* US = `api.zoom.us`
* EU = `eu01web.zoom.us`

## To run
* Install/Download python:
https://www.python.org/downloads/
* Install/Download pip
https://pip.pypa.io/en/stable/installing/
* Install deps:
`pip install pyjwt`
* Run the script:\
`python get-statistics.py 2020-01-01 2020-01-31`\
`python get-employee-members.py`\
`python fix-statistics-to-employee-only.py statistics-2020-01-01-2020-01-31.csv`
