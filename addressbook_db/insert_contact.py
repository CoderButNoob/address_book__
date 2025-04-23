from addressbook_db.manage_db import get_contact


def insert_contact(contact):
    conn = get_contact()
    cursor = conn.cursor()
    query = """
        INSERT INTO contacts (first_name, last_name, address, city, state, zip_code, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        contact.first_name, contact.last_name, contact.address,
        contact.city, contact.state, contact.zip_code,
        contact.phone, contact.email
    )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
