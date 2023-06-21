import pandas as pd
from db_connection import create_connection

def fetch_data():
    conn = create_connection()

    if conn is not None:
        query = """
            SELECT post_text, timestamp, sentiment_score 
            FROM your_table
        """
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            print("Error: ", e)
            return None
    else:
        print("No database connection established.")
        return None