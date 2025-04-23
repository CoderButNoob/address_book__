import mysql.connector 

def get_contact():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "PASSWORD",
        database="address_book_db"
    )