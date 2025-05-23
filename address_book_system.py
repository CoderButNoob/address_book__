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
            print("5. Sort Contact")
            print("6. Back to Main Menu")

            choice = input("Enter choice: ")

            if choice == "1":
                book.add_contact()  
            elif choice == "2":
                book.display_contacts()
            elif choice == "3":            
                book.edit_contacts()
            elif choice == "4":            
                book.delete_contact()
            elif choice == "6":
                break
            elif choice  == "5":
                book.sort_contact()
            else:
                print("Invalid choice.")
            
class AddressBookSearch(AddressBookSystem):
    def __init__(self):
        super().__init__()
        
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
    
    def view_by_city_or_state(self, count_only = False):
        if not self.books:
            print("No Book")
            return
        person_state = {}
        person_city = {}

        for book in self.books.values():
            for contact in book.details:
                city = contact.city.title()
                person_city.setdefault(city, []).append(contact)   

                state = contact.state.title()
                person_state.setdefault(state, []).append(contact)
            
        choice = int(input("\nEnter (1)-City (2)-State: "))
        if choice  == 1:
            for city , people in person_city.items():
                print(f"\n City :{city} ({len(people)} contact{'s' if len(people)>1 else ''})")
                if not count_only :
                    for person in people:
                        print(person)
            
        elif choice == 2:
            for state, people in person_state.items():
                print(f"\n State :{state} ({len(people)} contact{'s' if len(people)>1 else ''})")
                if not count_only :
                    for person in people:
                        print(person)
        else:
            print("Invalid Entry")
    
    def count_by_city_or_state(self):
        self.view_by_city_or_state(count_only=True)


        
            





        
        







