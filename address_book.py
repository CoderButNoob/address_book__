
from details import Details, get_contact_input

class AddressBook:
    def __init__(self):
        self.details =  [] #this help  in adding multiple contact in an perticular address book
    
    #the number of time we call it appends the data to the details list of an address-book
    def add_contact(self):
        print("\n Add New Contact")
        contact = get_contact_input()
        if contact is None:
            print("Print Contact not added due to validation error")
            return
        
        if any(c.first_name == contact.first_name and c.last_name == contact.last_name for  c in self.details):
            print("Contact already Exists")
        
        self.details.append(contact)
        print("Conatct Added Succesfully")
                    
    def display_contacts(self):
        if not self.details:
            print("\nEmpty Book...")
            return
        
        print("\n All Contacts")
        for i , detail in enumerate(self.details,1):
            print(f"\n Contact{i} : \n{detail}")
    
    def edit_contacts(self):
        name = input("Enter the first name of contact to edit")
        for detail in self.details:
            if detail.first_name.lower() == name.lower():
                print("Edit Data or Press Enter to keep the existing data...")

                updated_data = {
                    "first_name" : detail.first_name,
                    "last_name" : input("Edit Last Name [{detail.last_name}]: ") or detail.last_name,
                    "address" : input("Edit Address [{detail.address}]: ") or detail.address,
                    "city" : input("Edit City [{detail.city}]: ") or detail.city,
                    "state" : input("Edit state [{detail.state}]: ") or detail.state,
                    "zip_code" : input("Edit zip_code [{detail.zip_code}]: ") or detail.zip_code,
                    "phone" : input("Edit phone [{detail.phone}]: ") or detail.phone,
                    "email" : input("Edit email [{detail.email}]: ") or detail.email,                     
                }
            try:
                updated_data = Details(**updated_data)
                self.details[self.details.index(detail)] = updated_data
                print("Contact Updated")
            except Exception as e:
                print("Validation error" , e)
            return
        print("Contact Not Found")

    def delete_contact(self):
        name = input("Enter First Name of the contact to delete")
        for detail in self.details:
            if detail.first_name == name:
                confirm = input(f"Are you sure  you want to delete {detail.first_name}?? (y/n): ")
                if confirm == 'y':
                    self.details.remove(detail)
                    print("Contact Deleted")
                else:
                    print("Deletion Cancelled")
                return
        print("Contact Not Found")

    def sort_contacts(self):
        if not self.details:
            print("No Contact")
            return
        
        print("\nSort by:\n1. First Name\n2. City\n3. State\n4. Zip Code")
        choice = int(input("Enter Choice 1/2/3/4"))
        if choice == 1:
            self.details.sort(key = lambda contact :contact.first_name.lower())
            print("Sorted by First Name")
        elif choice == 2:
            self.details.sort(key = lambda contact: contact.city.lower())
            print("Sorted by City")
        elif choice == 3:
            self.details.sort(key = lambda contact: contact.state.lower())
            print("Sorted by State")
        elif choice == 4:
            self.details.sort(key = lambda contact: contact.zip_code.lower())
            print("Sorted by Zip Code")
        else:
            print("Invalid")

        


        
        


