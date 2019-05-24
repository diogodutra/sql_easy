# SQL Easy

SqlEasy is an interface to manipulate SQLite database from Python.

If you need to write or query directly the SQL with automatic commits right after then this is for you. It is intended to be used for applications where writing and quering a shared SQL file is necessary.

All instructions are operated directly in the SQL instead of Python. It means that if you issue the instruction `join` then it will actually execute the join commmand in the SQL cursor instead of using the NumPy or any other Python library. This approach guarantees that any modification performed recently by other users in the same database will be considered in your instruction.

## Examples

The `Main.py` shows one of the examples below.

Creating an empty database from scratch:
```
from sql_easy import SqlEasy

db = SqlEasy('my_sqlite.db')
```

Connecting to an existing database and create a table:
```
from sql_easy import SqlEasy

db = SqlEasy('my_sqlite.db')

db.create_table( 'Jobs'
                , 'id', 'INTEGER PRIMARY KEY'
                , 'profession', 'TEXT'
                )
db.add_row('Jobs', 'Politician')
db.add_row('Jobs', 'Writer')
db.add_row('Jobs', 'Actor/Actress')
```

Using a shared database while there is another user executing an active connection:
```
from sql_easy import SqlEasy

file_name = 'my_sqlite.db'
db = SqlEasy(file_name)
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
```
