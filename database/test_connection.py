import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    connection = psycopg2.connect(DATABASE_URL)

    print("✅ PostgreSQL connection successful!")

    cursor = connection.cursor()
    cursor.execute("SELECT version();")

    version = cursor.fetchone()
    print("PostgreSQL:", version[0])

    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Database connection failed:")
    print(e)