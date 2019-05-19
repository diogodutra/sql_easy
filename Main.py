import os
from sql_easy import SqlEasy

file_name = 'company.db'
try:
    os.remove(file_name)
except:
    print('Creating database named', file_name)

db = SqlEasy(file_name)

print('SQLite version: ', db.version())

db.create_table( 'Jobs'
                , 'id', 'INTEGER PRIMARY KEY'
                , 'profession', 'TEXT'
                )
db.add_row('Jobs', 'Politician')
db.add_row('Jobs', 'Writer')
db.add_row('Jobs', 'Actor/Actress')

db.create_table( 'Celebrities'
                , 'id', 'INTEGER PRIMARY KEY'
                , 'fname', 'VARCHAR(20)'
                , 'lname', 'VARCHAR(30)'
                , 'gender', 'CHAR(1)'
                , 'birth_date', 'DATE'
                , 'job_id', 'INT'
                )
db.add_row('Celebrities', 'William', 'Shakespeare', 'm', '1961-10-25', '2')
db.add_row('Celebrities', 'Frank',   'Schiller',    'm', '1955-08-17', '1')
db.add_row('Celebrities', 'Jane',    'Wall',        'f', '1989-03-14', '3')

db.del_rows('Celebrities', 'fname="Frank"')

table = db.join('Celebrities', 'Jobs', 'job_id', 'id'
                , columns='fname, lname, gender, profession')

for t in table:
    print(t)