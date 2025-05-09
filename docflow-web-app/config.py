import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-key")  # Default to avoid crashes
    DB_SERVER = os.getenv("DB_SERVER")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_DRIVER = os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}")
