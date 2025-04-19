from address_book_system import AddressBookSystem,AddressBookSearch

def main():
    print("Welcome to the Address Book System")
    system = AddressBookSystem()
    search = AddressBookSearch()

    while True:
        print("\nMenu")
        print("1. Create Address Book")
        print("2. List Address Book")
        print("3. Open Address Book")
        print("4. Search by City or State")
        print("5. View by City or State")
        print("6. Count by City or State")
        print("0. Exit")

        choice = int(input("Enter Your Choice:"))

        if choice == 1:
            system.create_book()
        elif choice == 2:
            system.list_book()
        elif choice == 3:
            system.operate_book()
        elif choice == 0:
            print("Goodbye")
            break
        elif choice == 4:
            search.search_by_city_state()
        elif choice == 5:
            search.view_by_city_or_state()
        elif choice == 6:
            search.count_by_city_or_state()
        else:
            print("Invalid Input")


if __name__ == "__main__":
    main()