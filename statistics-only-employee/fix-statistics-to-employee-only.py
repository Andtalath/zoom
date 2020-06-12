import sys
import csv
import re

try:
	zoom_file = sys.argv[1]
except:
	zoom_file = input("statistics-2019-06-01-2019-06-30.csv: ")
else:
	zoom_file = sys.argv[1]

zoom_employee = zoom_file[:-4]+"-only-employee.csv"

with open(zoom_employee, mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',')
    with open(zoom_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        line_count = 0
        fix_count = 0
        for row in readCSV:
            if line_count == 0:
                employee_writer.writerow(row)
            email = row[1]
            email_fix = re.split(r'\t+', email.rstrip('\t'))
            #print(email_fix)
            line_count += 1
            with open('employee.txt') as f:
                if email_fix[0] in f.read():
                    fix_count += 1
                    employee_writer.writerow(row)
    f.close()
print(f'Processed {line_count} lines. Total {fix_count} meetings with employee as host')
