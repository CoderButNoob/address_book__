from details import Details

class AddressBook:
    def __init__(self):
        self.details =  []
    
    def add_contact(self):
        print("\n Add New Contact")
        data = {
            "first_name": input("First Name: "),
            "last_name": input("Last Name:"),
            "address": input("Address: "),
            "city": input("City: "),
            "state": input("State: "),
            "zip_code": input("Zip Code: "),
            "phone": input("Phone Number: "),
            "email": input("Email: ")
        }

        try:
            detail = Details(**data)
            self.details.append(detail)
            print("Data Added !!!")
        except Exception as e:
            print("Validation Error: ",e)
    
    def display_contacts(self):
        if not self.details:
            print("\nEmpty Book...")
            return
        
        print("\n All Contacts")
        for i , detail in enumerate(self.details,1):
            print("\n Contact{i} : {detail}")
    
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
        
        


