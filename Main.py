import os
from sql_easy import SqlEasy

file_name = 'company.db'
try:
    os.remove(file_name)
except:
    print('Creating database named', file_name)

db = SqlEasy(file_name)

print('SQLite version: ', db.version())

table_name = 'employee'
db.create_table( table_name
                , 'staff_number', 'INTEGER PRIMARY KEY'
                , 'fname', 'VARCHAR(20)'
                , 'lname', 'VARCHAR(30)'
                , 'gender', 'CHAR(1)'
                , 'birth_date', 'DATE'
                )

db.add_row(table_name, 'William', 'Shakespeare', 'm', '1961-10-25')
db.add_row(table_name, 'Frank',   'Schiller',    'm', '1955-08-17')
db.add_row(table_name, 'Jane',    'Wall',        'f', '1989-03-14')

table = db.get_rows(table_name)
for t in table:
    print(t)

print()
row = db.get_rows(table_name, 'staff_number=2')
print(row)