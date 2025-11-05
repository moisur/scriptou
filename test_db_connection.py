import pymysql
import os

# Database credentials
DB_HOST = '109.234.162.77'
DB_PORT = 3306
DB_USER = 'gile7808_val'
DB_PASS = 'levelup2025'
DB_NAME = 'gile7808_scriptou'

try:
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected to the database!")
    conn.close()
except pymysql.Error as e:
    print(f"Error connecting to the database: {e}")
