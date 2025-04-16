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

