import psycopg2
import pandas as pd

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Articles (
            ArticleID SERIAL PRIMARY KEY, 
            URL TEXT NOT NULL UNIQUE, 
            Content TEXT, 
            SentimentScore FLOAT, 
            FeatureVector JSONB
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS SocialMediaPosts (
            PostID SERIAL PRIMARY KEY,
            ArticleID INT,
            Site TEXT,
            Content TEXT,
            SentimentScore FLOAT,
            Timestamp TIMESTAMP,
            FOREIGN KEY (ArticleID) REFERENCES Articles (ArticleID)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS NewsSitesArticles (
            ArticleID SERIAL PRIMARY KEY,
            RelatedArticleID INT,
            URL TEXT NOT NULL UNIQUE,
            Content TEXT,
            SentimentScore FLOAT,
            Timestamp TIMESTAMP,
            FOREIGN KEY (RelatedArticleID) REFERENCES Articles (ArticleID)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Trends (
            TrendID SERIAL PRIMARY KEY,
            ArticleID INT,
            TrendScore FLOAT,
            Timestamp TIMESTAMP,
            FOREIGN KEY (ArticleID) REFERENCES Articles (ArticleID)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Correlations (
            CorrelationID SERIAL PRIMARY KEY,
            ArticleID INT,
            CorrelationScore FLOAT,
            Timestamp TIMESTAMP,
            FOREIGN KEY (ArticleID) REFERENCES Articles (ArticleID)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PreviousTrends (
            PrevTrendID SERIAL PRIMARY KEY,
            ArticleID INT,
            PrevTrendScore FLOAT,
            Timestamp TIMESTAMP,
            FOREIGN KEY (ArticleID) REFERENCES Articles (ArticleID)
        )
    """)
    conn.commit()
    cur.close()

def insert_data(conn, table_name, data):
    cur = conn.cursor()
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cur.execute(query, tuple(data.values()))
    conn.commit()
    cur.close()

def fetch_data(conn, table_name, columns):
    cur = conn.cursor()
    column_names = ", ".join(columns)
    cur.execute(f"SELECT {column_names} FROM {table_name}")
    rows = cur.fetchall()
    cur.close()
    return rows

def update_data(conn, table_name, column, new_value, condition):
    cur = conn.cursor()
    cur.execute(f"UPDATE {table_name} SET {column} = %s WHERE {condition}", (new_value,))
    conn.commit()
    cur.close()