from address_book import AddressBook

class AddressBookSystem:
    def __init__(self):
        self.books =  {} #maintain a dictionary for address book

    def create_book(self):
        book = input("Enter name of New Address Book: ").strip()
        if book in self.books:
            print("Address Book alredy exists")
        else:
            self.books[book] = AddressBook()
            print(f"\nAddress Book created '{book}'")
    
    def list_book(self):
        if not self.books:
            print("No Address Book")
        else:
            print("\nAvailable Address Book: ")
            for book in self.books:
                print(f"{book}")

    def get_book(self):
        book = input("\nEnter the name of Address Book you want to open: ")
        return self.books.get(book)
    
    def operate_book(self):
        book = self.get_book()
        if not book :
            print("Address Book not found")
            return
        
        while True:
            
            print("\nMenu:")
            print("1. Add Contact")
            print("2. Display Contacts")
            print("3. Edit Contact")
            print("4. Delete Contact")
            print("5. Back to Main Menu")

            choice = input("Enter choice: ")

            if choice == "1":
                book.add_contact()  
            elif choice == "2":
                book.display_contacts()
            elif choice == "3":            
                book.edit_contacts()
            elif choice == "4":            
                book.delete_contact()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

    def search_by_city_state(self):
        if not self.books:
            print("No Book")
            return
        
        choice = int(input("\nEnter (1)-City (2)-State: "))
        if choice  == 1:
            key = "city"
        elif choice == 2:
            key = "state"
        else:
            print("Invalid Choice")
            return
        
        option = input(f"Enter {key.title()} to search: ")
        found = False

        for book_name , book in self.books.items():
            for contact in book.details:
                if getattr(contact,key) == option:
                    print(contact)
                    found = True
            
            if not found:
                print("Conatct Not found")


        
        







