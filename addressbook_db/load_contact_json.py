import json
from db_connection import connect

def load_contacts_from_json(filename="contacts.json", batch_size=1000):
    conn = connect()
    cursor = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    total = len(contacts)
    batch = []
    count = 0

    print(f"Total records: {total}")

    for idx, contact in enumerate(contacts, 1):
        batch.append(contact)

        if len(batch) >= batch_size:
            for c in batch:
                cursor.callproc('sp_add_contact', [
                    c['address_book_id'],
                    c['first_name'],
                    c['last_name'],
                    c['email'],
                    c['phone'],
                    c['address'],
                    c['city'],
                    c['state'],
                    c['zip']
                ])
            conn.commit()
            count += len(batch)
            print(f"Inserted {count}/{total} records...")
            batch.clear()

    if batch:
        for c in batch:
            cursor.callproc('sp_add_contact', [
                c['address_book_id'],
                c['first_name'],
                c['last_name'],
                c['email'],
                c['phone'],
                c['address'],
                c['city'],
                c['state'],
                c['zip']
            ])
        conn.commit()
        count += len(batch)
        print(f"Inserted {count}/{total} records (final batch).")

    cursor.close()
    conn.close()

    print("All contacts inserted successfully!")

if __name__ == "__main__":
    load_contacts_from_json()
