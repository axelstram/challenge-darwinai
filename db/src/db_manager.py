import psycopg2
import os
from dotenv import load_dotenv
from ..models.user import User
from ..models.expenses import Expense


class DatabaseManager:
    def __init__(self, database=None, host=None, port=None, user=None, password=None):
        if os.environ.get('ENV') != 'PRODUCTION':
            load_dotenv()

        self.conn = psycopg2.connect(
            host = host or os.environ.get('DB_HOST'),
            port = port or os.environ.get('DB_PORT'),
            user = user or os.environ.get('DB_USER'),
            password = password or os.environ.get('DB_PASSWORD'),
            database = database or os.environ.get('DB_DATABASE')
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        self.create_tables()

    def __exit__(self):
        self.close_connection()

    def create_tables(self):

        users_table_sql = '''
            CREATE TABLE IF NOT EXISTS users (
            "id" SERIAL PRIMARY KEY,
            "telegram_id" TEXT UNIQUE NOT NULL
            );'''

        expenses_table_sql = '''
            CREATE TABLE IF NOT EXISTS expenses (
                "id" SERIAL PRIMARY KEY,
                "user_id" INTEGER NOT NULL REFERENCES users("id"),
                "description" TEXT NOT NULL,
                "amount" MONEY NOT NULL,
                "category" TEXT NOT NULL,
                "added_at" TIMESTAMP NOT NULL
            );'''

        self.execute_query(users_table_sql)
        self.execute_query(expenses_table_sql)

        create_user_id_index_sql = '''CREATE INDEX IF NOT EXISTS user_id_idx
                                        ON expenses(user_id);'''

        self.execute_query(create_user_id_index_sql)

        self.conn.commit()

    def delete_tables(self):
        delete_expenses_sql = '''DROP TABLE IF EXISTS expenses;'''
        delete_usrs_sql = '''DROP TABLE IF EXISTS users;'''

        self.cursor.execute(delete_expenses_sql)
        self.cursor.execute(delete_usrs_sql)

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        
    def execute_query(self, query):
        try:
            self.cursor.execute(query)

            if 'SELECT' in query:
                return self.cursor.fetchall()
            else:
                #nothing to fetch
                return True
        except Exception as e:
            print(f"Error executing query: {e}")
            return False


    def insert_user(self, user):
        query = "INSERT INTO users (telegram_id) VALUES ({0}) ON CONFLICT DO NOTHING".format(user.get_telegram_id())

        return self.execute_query(query)

    def user_is_whitelisted(self, user):
        query = """SELECT id FROM users
                        WHERE telegram_id = '{0}';""".format(user.get_telegram_id())

        result = self.execute_query(query)

        if result:
            return len(result) == 1
        else:
            return False

    def insert_expense(self, expense):
        try:
            query = """SELECT id FROM users
                        WHERE telegram_id = '{0}';""".format(expense.user_telegram_id)

            result = self.execute_query(query)

            id = result[0][0]

            query = """INSERT INTO expenses (user_id, description, amount, category, added_at) 
                        VALUES (%i, '%s', %i, '%s', '%s')""" % (int(id), expense.description, float(expense.amount), expense.category, expense.added_at)

            self.execute_query(query)
            
            return True
        except Exception as e:
            print(f"Error adding expenses: {e}")
            return False

    def get_expenses_from_user(self, user):
        try:
            query = """SELECT id FROM users
                        WHERE telegram_id = '{0}';""".format(user.get_telegram_id())

            result = self.execute_query(query)

            id = result[0][0]

            query = """SELECT * FROM expenses
                        WHERE user_id = '{0}';""".format(id)

            result = self.execute_query(query)
            
            return result
            
        except Exception as e:
            print(f"Error getting expenses from user: {e}")
            return False

