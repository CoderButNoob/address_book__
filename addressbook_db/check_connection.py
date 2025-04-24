import mysql.connector, sys

try:
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="PASSWORD",
        database="address_book_db"
    )
    print("✅ Connected!", conn.get_server_info())  # ← fixed line
    conn.close()
except mysql.connector.Error as e:
    print("❌ Connection failed:", e)
