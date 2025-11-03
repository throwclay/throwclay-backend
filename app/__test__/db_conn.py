
import psycopg
from dotenv import load_dotenv
import os
from psycopg.rows import dict_row

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # e.g. postgresql://USER:PASS@HOST:6543/postgres

# Connect to the database
try:

    connection = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")