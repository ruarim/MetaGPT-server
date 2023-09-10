import psycopg2


class Db:
    def __init__(self, credentials: str):
        self.connection = psycopg2.connect(credentials)
        self.cursor = self.connection.cursor()

    def query(self, sql: str, params: tuple = None):
        try:
            self.cursor.execute(sql, params)
            if sql.strip().lower().startswith('select'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            raise e

    def save(self, table_name, data):
        if 'id' in data and data['id'] is not None:
            self._update_record(table_name, data)
        else:
            self._insert_record(table_name, data)

    def _insert_record(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        values = tuple(data.values())

        self.execute_query(query, values)

    def _update_record(self, table_name, data):
        if 'id' not in data or data['id'] is None:
            raise ValueError(
                "To update a record, 'id' must be provided in the data.")

        update_columns = ', '.join(
            [f"{key} = %s" for key in data.keys() if key != 'id'])
        
        query = f"UPDATE {table_name} SET {update_columns} WHERE id = %s;"
        values = tuple([data[key]
                        for key in data.keys() if key != 'id'] + [data['id']])

        self.execute_query(query, values)
