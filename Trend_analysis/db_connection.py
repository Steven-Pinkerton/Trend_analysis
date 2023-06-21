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