import mysql.connector as conn

class Database:
    def __init__(self, host='localhost', user='root', password='mySQLroot#24', database='testing'):
        self.conn = conn.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return self.cursor
        except conn.Error as err:
            print(f"Error: {err}")

    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except conn.Error as err:
            print(f"Error: {err}")
            return []

    def close(self):
        self.conn.close()
