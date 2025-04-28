from db_connection import connect
from schema_manager import ensure_schema
from generate_json import generate_json
from load_contact_json import load_contacts_from_json

def insert_address_books():
    """Insert initial address books to satisfy foreign key constraint."""
    conn = connect()
    cursor = conn.cursor()
    names = ["Personal", "Work", "Family", "Friends"]  

    for name in names:
        cursor.execute("INSERT IGNORE INTO address_books (name) VALUES (%s)", (name,))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted address_books: {names}")

def main():
    print("Step 1: Creating schema (Tables, Stored Procedures, Triggers)...")
    ensure_schema()

    print("\nStep 2: Inserting address books (if not already)...")
    insert_address_books()

    print("\nStep 3: Generating contacts JSON file...")
    generate_json(filename="contacts.json", total_records=100000, max_address_book_id=4)

    print("\nStep 4: Loading contacts into database...")
    load_contacts_from_json(filename="contacts.json", batch_size=1000)

    print("\nAll Done Successfully!")

if __name__ == "__main__":
    main()
