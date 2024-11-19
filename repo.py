import os
import mysql.connector
from dotenv import load_dotenv 

class Repo:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        try:
            # Establish connection
            self.conn = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            self.cursor = self.conn.cursor()

            # Create database if not exists
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS yadtq")
            self.conn.database = 'yadtq'

            # Create table if not exists
            create_table_query = """
                CREATE TABLE IF NOT EXISTS tt_request_status (
                    request_id VARCHAR(255) PRIMARY KEY,
                    status VARCHAR(255),
                    task_type VARCHAR(255),
                    result FLOAT
                )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            

    def write_status(self, request_id, status, task_type=None, result=None):
        """Insert initial status of the request, along with task type and result."""
        query = """
            INSERT INTO tt_request_status (request_id, status, task_type, result) 
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (request_id, status, task_type, result))
        self.conn.commit()

    def update_status(self, request_id, status, task_type=None, result=None):
        """Update the status, task type, and result of the request."""
        query = """
            UPDATE tt_request_status 
            SET status=%s, task_type=%s, result=%s 
            WHERE request_id=%s
        """
        self.cursor.execute(query, (status, task_type, result, request_id))
        self.conn.commit()

    def query_status(self, request_id):
        """Retrieve the current status of the request."""
        query = "SELECT status, task_type, result FROM tt_request_status WHERE request_id=%s"
        self.cursor.execute(query, (request_id,))
        result = self.cursor.fetchone()
        return result if result else ("Not Found", None, None)

    def __del__(self):
        """Cleanup MySQL connection on object destruction."""
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            # print("MySQL connection closed.")