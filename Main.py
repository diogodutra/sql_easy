import os
import uuid
from sql_easy import SqlEasy

unique_name = './data/demo_' + str(uuid.uuid4()) + '.db'
file_name = unique_name

db = SqlEasy(file_name) # Same syntax to connect to an existent database
db.create_table( 'Jobs'
                , 'id', 'INTEGER PRIMARY KEY'
                , 'profession', 'TEXT'
                )
db.add_row('Jobs', 'Politician')
db.add_row('Jobs', 'Writer')
db.add_row('Jobs', 'Actor/Actress')

# Now we will use another connection to database in order
# to show that it works well even with multiple connections
# writing in the same file at the same time.
db_other_connection = SqlEasy(file_name)
db_other_connection.create_table( 'Celebrities'
                , 'id', 'INTEGER PRIMARY KEY'
                , 'fname', 'VARCHAR(20)'
                , 'lname', 'VARCHAR(30)'
                , 'gender', 'CHAR(1)'
                , 'birth_date', 'DATE'
                , 'job_id', 'INT'
                )
db_other_connection.add_row('Celebrities', 'William', 'Shakespeare', 'm', '1961-10-25', '2')
db_other_connection.add_row('Celebrities', 'Frank',   'Schiller',    'm', '1955-08-17', '1')
db_other_connection.add_row('Celebrities', 'Jane',    'Wall',        'f', '1989-03-14', '3')
db_other_connection.del_rows('Celebrities', where='fname="Frank"')

# Mind that now we will use the 1st connection to check if
# it is capable of accessing the modifications performed
# by the other 2nd connection
table = db.join('Celebrities', 'Jobs', 'job_id', 'id'
                , columns='fname, lname, gender, profession'
                , sort_column='gender')

for t in table:
    print(t)