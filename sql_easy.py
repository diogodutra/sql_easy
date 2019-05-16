import sqlite3

class SqlEasy(object):
    filename = ''
    connection = cursor = None
    tables = []
    col_labels = []
    col_types = []
    _command_create_table = 'CREATE TABLE {table} ({arguments});'
    _command_insert_data = 'INSERT INTO {table} ({labels}) VALUES ({values});'
    _command_query_table = 'SELECT * FROM {table}'
    _arg_labels = []

    def __init__(self, filename):
        self.filename = filename
        self.open_sql()

    def __del__(self):
        self.connection.close()

    def open_sql(self):
        #TODO: throw error when filename already exist
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, *attributes):
        #TODO: assert table exists
        #TODO: assert pair entries of attributes
        #TODO: assert valid labels and type_sql pairs
        self.tables.append(table_name)
        arguments = ''
        arg_labels = ''
        labels = []
        types_sql = []
        while (len(attributes)>0):
            label, type_sql, *attributes = attributes
            labels.append(label)
            types_sql.append(type_sql)
            arg_labels = arg_labels + label + ', '
            arguments = arguments + label + ' ' + type_sql + ', '

        self.col_labels.append(labels)
        self.col_types.append(types_sql)

        arg_labels = arg_labels[:-2]
        self._arg_labels.append(arg_labels)

        arguments = arguments[:-2]
        command = self._command_create_table.format(table=table_name, arguments=arguments)
        self.cursor.execute(command)
        self.connection.commit()

    def add_row(self, table_name, *values):
        #TODO: assert table exists
        #TODO: assert length of values
        arg_values = ''
        i_value = 0
        index_table = self.tables.index(table_name)
        for i_type in self.col_types[index_table]:
            is_primary_key = 'PRIMARY KEY' in i_type
            if (is_primary_key):
                arg_values = arg_values + 'NULL' + ', '
            else:
                arg_values = arg_values + '"' + str(values[i_value]) + '"' + ', '
                i_value += 1

        arg_values = arg_values[:-2]

        command = self._command_insert_data.format(table=table_name
            , labels=self._arg_labels[index_table], values=arg_values)
        
        self.cursor.execute(command)
        self.connection.commit()
        
    def get_rows(self, table_name):
        command = self._command_query_table.format(table=table_name)
        self.cursor.execute(command)
        return self.cursor.fetchall()