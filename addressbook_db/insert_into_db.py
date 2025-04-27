from __future__ import annotations
from mysql.connector import Error
from .db_connection import connect
from details import Details
from .table_schema import TableSchema

# # ---------- DDL ----------
# DDL_ADDRESSBOOK = """
# CREATE TABLE IF NOT EXISTS address_books (
#     id   INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) UNIQUE NOT NULL
# )
# """

# DDL_CONTACT = """
# CREATE TABLE IF NOT EXISTS contacts (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     address_book_id INT NOT NULL,
#     first_name VARCHAR(50),
#     last_name  VARCHAR(50),
#     email      VARCHAR(100),
#     phone      VARCHAR(15),
#     address    VARCHAR(255),
#     city       VARCHAR(50),
#     state      VARCHAR(50),
#     zip        VARCHAR(10),
#     FOREIGN KEY (address_book_id)
#         REFERENCES address_books(id) ON DELETE CASCADE
# )
# """

def _ensure_schema(cur):
    print("Creating Tables with Queries:\n")
    for table_key in TableSchema.table_schema.keys():
        query = TableSchema.get_create_statement(table_key)
        print(f"{TableSchema.get_table_name(table_key)}:\n{query}\n")
        cur.execute(query)



# ---------- Address Book ----------
def create_address_book(name: str) -> int | None:
    with connect() as conn:
        if conn is None: return None
        cur = conn.cursor()
        _ensure_schema(cur)
        try:
            cur.execute("INSERT IGNORE INTO address_books (name) VALUES (%s)", (name,))
            conn.commit()
            cur.execute("SELECT id FROM address_books WHERE name=%s", (name,))
            (ab_id,) = cur.fetchone()
            return ab_id
        except Error as e:
            print("DB error:", e)
            return None
        finally:
            cur.close()

def list_address_books() -> list[tuple[int, str]]:
    with connect() as conn:
        if conn is None: return []
        cur = conn.cursor()
        _ensure_schema(cur)
        cur.execute("SELECT id, name FROM address_books ORDER BY name")
        rows = cur.fetchall()
        cur.close()
        return rows

# ---------- Contacts ----------
def add_contact(book_id: int, detail: Details) -> None:
    with connect() as conn:
        if conn is None: return
        cur = conn.cursor()
        _ensure_schema(cur)
        cols = (
            "address_book_id, first_name, last_name, email, phone, "
            "address, city, state, zip"
        )
        vals = (
            book_id,
            detail.first_name,
            detail.last_name,
            detail.email,
            detail.phone,
            detail.address,
            detail.city,
            detail.state,
            detail.zip_code,
        )
        cur.execute(
            f"INSERT INTO contacts ({cols}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            vals,
        )
        conn.commit()
        cur.close()

def fetch_contacts(book_id: int) -> list[Details]:
    with connect() as conn:
        if conn is None: return []
        cur = conn.cursor(dictionary=True)  # returns dict rows
        cur.execute("SELECT * FROM contacts WHERE address_book_id=%s", (book_id,))
        rows = cur.fetchall()
        cur.close()
    return [
        Details(
            first_name=r["first_name"],
            last_name=r["last_name"],
            address=r["address"],
            city=r["city"],
            state=r["state"],
            zip_code=r["zip"],
            phone=r["phone"],
            email=r["email"],
        )
        for r in rows
    ]
def update_contact(book_id: int, old: Details, new: Details) -> None:
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE contacts
            SET first_name=%s, last_name=%s, email=%s, phone=%s,
                address=%s, city=%s, state=%s, zip=%s
            WHERE address_book_id=%s AND first_name=%s AND last_name=%s
            """,
            (
                new.first_name, new.last_name, new.email, new.phone,
                new.address, new.city, new.state, new.zip_code,
                book_id, old.first_name, old.last_name,
            ),
        )
        conn.commit()
        cur.close()

def delete_contact_db(book_id: int, detail: Details) -> None:
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM contacts
            WHERE address_book_id=%s AND first_name=%s AND last_name=%s
            """,
            (book_id, detail.first_name, detail.last_name),
        )
        conn.commit()
        cur.close()
