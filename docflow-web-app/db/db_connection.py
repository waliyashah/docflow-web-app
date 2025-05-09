# Description: This file contains the code to establish a connection to the SQL Server database.
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_DATABASE')};"
            f"UID={os.getenv('DB_USERNAME')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None
