
# from details import Details, get_contact_input
# from file_manager.file_manager_txt import  AddressBookFileManager
# from file_manager.file_manager_csv import AddressBookFileManagerCSV
# from file_manager.file_manager_json import AddressBookFileManagerJSON
# from addressbook_db.insert_into_db import (
#     create_address_book,
#     list_address_books,
#     add_contact,
#     fetch_contacts,
# )


# class AddressBook:
#     def __init__(self):
#         self.details =  [] #this help  in adding multiple contact in an perticular address book
    
#     #the number of time we call it appends the data to the details list of an address-book
#     def add_contact(self):
#         print("\n Add New Contact")
#         contact = get_contact_input()
#         if contact is None:
#             print("Print Contact not added due to validation error")
#             return
        
#         if any(c.first_name == contact.first_name and c.last_name == contact.last_name for  c in self.details):
#             print("Contact already Exists")
        
#         self.details.append(contact)
#         print("Conatct Added Succesfully")

#         insert_contact(contact)

#         self.add_to_txt()
#         self.write_csv()
#         self.write_json()
        
        
    
#     def add_to_txt(self , filename = "address_book.txt"):
#         AddressBookFileManager.write_detail(self.details,filename)
    
#     def read_from_txt(self , filename = "address_book.txt"):
#         self.details = AddressBookFileManager.read_details(filename)
    
#     def write_csv(self , filename = "address_book.csv"):
#         AddressBookFileManagerCSV.write_csv(self.details, filename)
    
#     def read_csv(self , filename = "address_book.csv"):
#         AddressBookFileManagerCSV.read_csv(self.details, filename)
    
#     def write_json(self, filename="address_book.json"):
#         AddressBookFileManagerJSON.write_json(self.details, filename)

#     def read_json(self, filename="address_book.json"):
#         self.details = AddressBookFileManagerJSON.read_json(filename) 
    

                    
#     def display_contacts(self):
#         if not self.details:
#             print("\nEmpty Book...")
#             return
        
#         print("\n All Contacts")
#         for i , detail in enumerate(self.details,1):
#             print(f"\n Contact{i} : \n{detail}")
    
#     def edit_contacts(self):
#         name = input("Enter the first name of contact to edit")
#         for detail in self.details:
#             if detail.first_name.lower() == name.lower():
#                 print("Edit Data or Press Enter to keep the existing data...")

#                 updated_data = {
#                     "first_name" : detail.first_name,
#                     "last_name" : input("Edit Last Name [{detail.last_name}]: ") or detail.last_name,
#                     "address" : input("Edit Address [{detail.address}]: ") or detail.address,
#                     "city" : input("Edit City [{detail.city}]: ") or detail.city,
#                     "state" : input("Edit state [{detail.state}]: ") or detail.state,
#                     "zip_code" : input("Edit zip_code [{detail.zip_code}]: ") or detail.zip_code,
#                     "phone" : input("Edit phone [{detail.phone}]: ") or detail.phone,
#                     "email" : input("Edit email [{detail.email}]: ") or detail.email,                     
#                 }
#             try:
#                 updated_data = Details(**updated_data)
#                 self.details[self.details.index(detail)] = updated_data
#                 print("Contact Updated")
#             except Exception as e:
#                 print("Validation error" , e)
#             return
#         print("Contact Not Found")

#     def delete_contact(self):
#         name = input("Enter First Name of the contact to delete")
#         for detail in self.details:
#             if detail.first_name == name:
#                 confirm = input(f"Are you sure  you want to delete {detail.first_name}?? (y/n): ")
#                 if confirm == 'y':
#                     self.details.remove(detail)
#                     print("Contact Deleted")
#                 else:
#                     print("Deletion Cancelled")
#                 return
#         print("Contact Not Found")

#     def sort_contacts(self):
#         if not self.details:
#             print("No Contact")
#             return
        
#         print("\nSort by:\n1. First Name\n2. City\n3. State\n4. Zip Code")
#         choice = int(input("Enter Choice 1/2/3/4"))
#         if choice == 1:
#             self.details.sort(key = lambda contact :contact.first_name.lower())
#             print("Sorted by First Name")
#         elif choice == 2:
#             self.details.sort(key = lambda contact: contact.city.lower())
#             print("Sorted by City")
#         elif choice == 3:
#             self.details.sort(key = lambda contact: contact.state.lower())
#             print("Sorted by State")
#         elif choice == 4:
#             self.details.sort(key = lambda contact: contact.zip_code.lower())
#             print("Sorted by Zip Code")
#         else:
#             print("Invalid")

        


        
        

# address_book.py
from details import Details, get_contact_input
from addressbook_db.insert_into_db import (
    add_contact,          # writes one contact
    fetch_contacts,       # returns list[Details]
    update_contact,       # ← you'll need to add these two helpers
    delete_contact_db,    #   to insert_into_db.py
)

class AddressBook:
    """
    Represents a single address‑book (row in `address_books` table).

    :param db_id: primary‑key id in MySQL
    """
    def __init__(self, db_id: int):
        self.db_id = db_id
        # hydrate the object from DB
        self.details: list[Details] = fetch_contacts(db_id)

    # ---------- ADD ----------
    def add_contact(self):
        print("\nAdd New Contact")
        contact = get_contact_input()
        if contact is None:
            print("Contact not added due to validation error.")
            return

        if any(c.first_name == contact.first_name and
               c.last_name  == contact.last_name for c in self.details):
            print("Contact already exists.")
            return

        add_contact(self.db_id, contact)   # ← persists to MySQL
        self.details.append(contact)       # update in‑memory cache
        print("✅ Contact added successfully")

    # ---------- DISPLAY ----------
    def display_contacts(self):
        if not self.details:
            print("\nEmpty Book...")
            return
        print("\nAll Contacts")
        for i, detail in enumerate(self.details, 1):
            print(f"\nContact {i}:\n{detail}")

    # ---------- EDIT ----------
    def edit_contacts(self):
        name = input("Enter the first name of contact to edit: ").strip()
        for idx, detail in enumerate(self.details):
            if detail.first_name.lower() == name.lower():
                print("Edit field or press Enter to keep existing value...")

                updated_data = {
                    "first_name": detail.first_name,
                    "last_name":  input(f"Last Name [{detail.last_name}]: ") or detail.last_name,
                    "address":    input(f"Address   [{detail.address}]: ")   or detail.address,
                    "city":       input(f"City      [{detail.city}]: ")      or detail.city,
                    "state":      input(f"State     [{detail.state}]: ")     or detail.state,
                    "zip_code":   input(f"Zip Code  [{detail.zip_code}]: ")  or detail.zip_code,
                    "phone":      input(f"Phone     [{detail.phone}]: ")     or detail.phone,
                    "email":      input(f"Email     [{detail.email}]: ")     or detail.email,
                }
                try:
                    updated = Details(**updated_data)
                    update_contact(self.db_id, detail, updated)  # DB write
                    self.details[idx] = updated                  # cache write
                    print("Contact updated")
                except Exception as e:
                    print("Validation error →", e)
                return
        print("Contact not found")

    # ---------- DELETE ----------
    def delete_contact(self):
        name = input("Enter first name of the contact to delete: ").strip()
        for detail in self.details:
            if detail.first_name.lower() == name.lower():
                if input(f"Delete {detail.first_name}? (y/n): ").lower() == "y":
                    delete_contact_db(self.db_id, detail)   # DB delete
                    self.details.remove(detail)             # cache delete
                    print("Contact deleted")
                else:
                    print("Deletion cancelled")
                return
        print("Contact not found")

    # ---------- SORT ----------
    def sort_contacts(self):
        if not self.details:
            print("No contact")
            return
        print("\nSort by:\n1. First Name\n2. City\n3. State\n4. Zip Code")
        choice = input("Enter choice 1/2/3/4: ").strip()
        key_fn = {
            "1": lambda c: c.first_name.lower(),
            "2": lambda c: c.city.lower(),
            "3": lambda c: c.state.lower(),
            "4": lambda c: c.zip_code,
        }.get(choice)
        if key_fn is None:
            print("Invalid choice")
            return
        self.details.sort(key=key_fn)
        print("Sorted.")

