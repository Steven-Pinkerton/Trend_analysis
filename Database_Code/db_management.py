import psycopg2
import pandas as pd

class DatabaseConnection:
    def __init__(self, dbname, user, password, host):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.conn = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            print("Connection successful!")
            return self.conn
        except psycopg2.Error as e:
            print(f"Unable to connect to the database: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            try:
                self.conn.close()
                print("Connection closed!")
            except psycopg2.Error as e:
                print(f"Error while closing connection: {e}")

def create_tables(conn):
    CREATE TABLE Articles (
        ArticleID SERIAL PRIMARY KEY, 
        URL TEXT NOT NULL UNIQUE, 
        Content TEXT, 
        SentimentScore FLOAT, 
        FeatureVector JSONB
        );
    
    

def insert_data(conn, table_name, data):
#Write SQL command to insert data into specified table

def fetch_data(conn, table_name, columns):
#Write SQL command to fetch specified columns from specified table

def update_data(conn, table_name, column, new_value, condition):
#Write SQL command to update specified column in specified table