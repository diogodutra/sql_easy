import sqlite3

class SqlEasy(object):
    filename = ''
    connection = cursor = None
    __index_column_key = 5
    __index_column_id = 0
    __index_column_label = 1
    __sql_key_code = 1
    __command_get_version = 'SELECT SQLITE_VERSION()'
    __command_create_table = 'CREATE TABLE {table} ({arguments})'
    __command_insert_data = 'INSERT INTO {table} ({labels}) VALUES ({values})'
    __command_query_table = 'SELECT {columns} FROM {table}'
    __command_where = ' WHERE {filter}'
    __command_sort = ' ORDER BY {column} {order}'
    __command_count_rows = 'SELECT count(*) FROM {table}'
    __command_del_rows = 'DELETE FROM {table}'
    __command_join_tables = 'SELECT {columns} FROM {table_left} {join_type} JOIN {table_right} ON {table_left}.{key_left} = {table_right}.{key_right}'
    __command_get_table_names = 'SELECT name FROM sqlite_master WHERE type="table"'
    __command_get_columnn_names = 'PRAGMA table_info("{table}")'

    def __init__(self, filename):
        self.filename = filename
        self.open_sql()

    def __del__(self):
        self.connection.close()

    def __add_where(self, filter):
        result = ''
        if (filter is not None):
            result += self.__command_where.format(filter=filter)

        return result

    def __add_sort(self, column, ascending):
        result = ''
        if (ascending): order = 'ASC'
        else: order = 'DESC'
        
        if (column is not None):
            result += self.__command_sort.format(column=column, order=order)

        return result

    def fetch(self, command):
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def sqlite_version(self):
        command = self.__command_get_version
        self.cursor.execute(command)
        return self.cursor.fetchone()[0]

    def open_sql(self):
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, *attributes):
        #TODO: assert pair entries of attributes
        #TODO: assert valid labels and type_sql pairs
        arguments = ''
        labels = []
        types_sql = []
        while (len(attributes)>0):
            label, type_sql, *attributes = attributes
            labels.append(label)
            types_sql.append(type_sql)
            arguments = arguments + label + ' ' + type_sql + ', '

        arguments = arguments[:-2]
        command = self.__command_create_table.format(table=table_name, arguments=arguments)
        self.cursor.execute(command)
        self.connection.commit()

    def add_row(self, table_name, *values):
        #TODO: assert length of values
        arg_values = ''
        i_value = 0
        i_primary_key = self.key_index(table_name)
        for i_col in range(self.count_cols(table_name)):
            is_primary_key = (i_primary_key == i_col)
            if (is_primary_key):
                arg_values = arg_values + 'NULL' + ', '
            else:
                arg_values = arg_values + '"' + str(values[i_value]) + '"' + ', '
                i_value += 1

        arg_values = arg_values[:-2]

        str_column_labels_with_commas = ', '.join(self.column_names(table_name))
        command = self.__command_insert_data.format(table=table_name
            , labels=str_column_labels_with_commas, values=arg_values)
        
        self.cursor.execute(command)
        self.connection.commit()
        
    def get_table(self, table_name, columns='*', where=None
                , sort_column=None, ascending=True):
        command = self.__command_query_table.format(table=table_name, columns=columns)
        command += self.__add_sort(sort_column, ascending)
        command += self.__add_where(where)
            
        self.cursor.execute(command)
        
        result = self.cursor.fetchall()
        if (len(result)==1):
            result = result[0]
            
        return result

    def table_names(self):
        command = self.__command_get_table_names
        self.cursor.execute(command)
        result = [x[0] for x in self.cursor.fetchall()]
        return result

    def column_names(self, table_name):
        command = self.__command_get_columnn_names.format(table=table_name)
        self.cursor.execute(command)
        result = [x[1] for x in self.cursor.fetchall()]
        return result

    def column_types(self, table_name):
        command = self.__command_get_columnn_names.format(table=table_name)
        self.cursor.execute(command)
        result = [x[2] for x in self.cursor.fetchall()]
        return result

    def key_index(self, table_name):
        command = self.__command_get_columnn_names.format(table=table_name)
        self.cursor.execute(command)
        result = None
        for column_info in self.cursor.fetchall():
            is_primary_key = (column_info[self.__index_column_key]==self.__sql_key_code)
            if (is_primary_key):
                result = column_info[self.__index_column_id]
                break

        return result

    def key_name(self, table_name):
        command = self.__command_get_columnn_names.format(table=table_name)
        self.cursor.execute(command)
        result = None
        for column_info in self.cursor.fetchall():
            is_primary_key = (column_info[self.__index_column_key]==self.__sql_key_code)
            if (is_primary_key):
                result = column_info[self.__index_column_label]
                break

        return result

    def count_cols(self, table_name):
        command = self.__command_get_columnn_names.format(table=table_name)
        self.cursor.execute(command)
        result = len(self.cursor.fetchall())
        return result
        
    def count_rows(self, table_name, where=None, sort_column=None, ascending=True):
        command = self.__command_count_rows.format(table=table_name)
        command += self.__add_sort(sort_column, ascending)
        command += self.__add_where(where)

        self.cursor.execute(command)
        return self.cursor.fetchall()[0][0]

    def del_rows(self, table_name, where=None):
        command = self.__command_del_rows.format(table=table_name)
        command += self.__add_where(where)
    
        self.cursor.execute(command)
        self.connection.commit()

    def join(self, table_left, table_right, key_left, key_right
            , columns='*', join_type='INNER', sort_column=None, ascending=True):
        command = self.__command_join_tables.format(table_left=table_left
            , table_right=table_right
            , columns=columns
            , join_type=join_type
            , key_left=key_left
            , key_right=key_right
            )
        command += self.__add_sort(sort_column, ascending)
    
        self.cursor.execute(command)
        return self.cursor.fetchall()