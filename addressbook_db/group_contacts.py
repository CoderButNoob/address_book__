# import csv
# from db_connection import connect

# def group_contact(filename="group_contact.csv"):
#     conn = connect()
#     cursor = conn.cursor(dictionary = True)

#     query = """
#             select b.name as addressbook_name,
#             c.first_name , c.last_name , c.email , c.phone , c.address , c.city , c.state , c.zip
#             from contacts c
#             join address_books b
#             on c.address_book_id = b.id
#             order by b.name , c.first_name
#             """
    
#     cursor.execute(query)
#     rows = cursor.fetchall()

#     if not rows:
#         print("No contact found")
#         return

#     with open(filename , "w") as file :
#         writer = csv.writer(file)
#         writer.writerow(["AddressBook", "First Name" , "Last Name" , "Email", "Phone" , "Address", "City", "State", "Zip"])

#         for row in rows:
#             writer.writerow([
#                 row["addressbook_name"],
#                 row["first_name"],
#                 row["last_name"],
#                 row["email"],
#                 row["phone"],
#                 row["address"],
#                 row["city"],
#                 row["state"],
#                 row["zip"]
#             ])
    
#     cursor.close()
#     conn.close()

#     print(f"Data Added to {filename}")

import csv
from db_connection import connect

def group_contact(book_name: str):
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    cursor.callproc("sp_get_contact_csv", [book_name])

    for result in cursor.stored_results():
        rows = result.fetchall()

    if not rows:
        print(f"No contacts found in address book: {book_name}")
        return

    
    safe_name = book_name.strip().replace(" ", "_").lower()
    filename = f"{safe_name}_contacts.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Address Book", "First Name", "Last Name", "Email",
            "Phone", "Address", "City", "State", "Zip"
        ])
        for row in rows:
            writer.writerow([
                row["AddressBook_Name"],
                row["First Name"],
                row["Last Name"],
                row["Email"],
                row["Phone"],
                row["Address"],
                row["City"],
                row["State"],
                row["Zip"]
            ])

    print(f"Exported contacts for '{book_name}' to file: {filename}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    name = input("Enter Address Book Name to export contacts: ")
    group_contact(name)
