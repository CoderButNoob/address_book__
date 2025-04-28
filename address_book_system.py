# address_book_system.py
from addressbook_db.insert_into_db import (
    create_address_book,
    list_address_books,
    add_contact,
    fetch_contacts,
)
from address_book import AddressBook, get_contact_input


class AddressBookSystem:
    """CLI controller that talks to MySQL‑backed AddressBook objects."""

    def __init__(self) -> None:
        # cache: {name -> AddressBook instance}
        self.books: dict[str, AddressBook] = {}

    # ---------- Address‑Book CRUD ---------- #
    def create_book(self) -> None:
        name = input("Enter name of New Address Book: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        ab_id = create_address_book(name)
        if ab_id:
            self.books[name] = AddressBook(db_id=ab_id)
            print(f"✅ Address Book '{name}' created (id {ab_id}).")
        else:
            print(" Address Book already exists or DB error.")

    def list_book(self) -> None:
        rows = list_address_books()
        if not rows:
            print("No Address Books in DB.")
            return

        print("\nAvailable Address Books:")
        for _id, nm in rows:
            print(f"{_id:>3}  {nm}")

    def _load_book(self, name: str) -> AddressBook | None:
        """Lazy‑load an AddressBook instance from DB if not cached."""
        if name in self.books:
            return self.books[name]

        lookup = {nm: _id for _id, nm in list_address_books()}
        if name not in lookup:
            return None

        self.books[name] = AddressBook(db_id=lookup[name])
        return self.books[name]

    def get_book(self) -> AddressBook | None:
        name = input("\nEnter the name of Address Book you want to open: ").strip()
        return self._load_book(name)

    # ---------- Main interaction loop ---------- #
    def operate_book(self) -> None:
        book = self.get_book()
        if not book:
            print("Address Book not found")
            return

        while True:
            print(
                "\nMenu:\n"
                "1. Add Contact\n"
                "2. Display Contacts\n"
                "3. Edit Contact\n"
                "4. Delete Contact\n"
                "5. Sort Contact\n"
                "6. Back to Main Menu"
            )

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self._add_contact_flow(book)
            elif choice == "2":
                book.display_contacts()
            elif choice == "3":
                book.edit_contacts()
            elif choice == "4":
                book.delete_contact()
            elif choice == "5":
                book.sort_contacts()
            elif choice == "6":
                break
            else:
                print("Invalid choice.")

    # ---------- Helpers ---------- #
    def _add_contact_flow(self, book: AddressBook) -> None:
        contact = get_contact_input()
        if contact is None:
            print("Contact not added due to validation error.")
            return

        # Persist to DB then update in‑memory cache
        add_contact(book.db_id, contact)
        book.details.append(contact)
        print("✅ Contact saved")


# --------- OPTIONAL: Search functionality re‑using the same cache --------- #
class AddressBookSearch(AddressBookSystem):
    """Extends AddressBookSystem with city/state search utilities."""

    def search_by_city_state(self) -> None:
        if not self.books:
            print("No Book")
            return

        try:
            choice = int(input("\nEnter (1)-City (2)-State: "))
        except ValueError:
            print("Invalid entry.")
            return

        key = "city" if choice == 1 else "state" if choice == 2 else None
        if not key:
            print("Invalid choice")
            return

        option = input(f"Enter {key.title()} to search: ").strip()
        found = False

        for book in self.books.values():
            for contact in book.details:
                if getattr(contact, key).lower() == option.lower():
                    print(contact)
                    found = True

        if not found:
            print("Contact Not found")

    def view_by_city_or_state(self, count_only: bool = False) -> None:
        if not self.books:
            print("No Book")
            return

        person_state: dict[str, list] = {}
        person_city: dict[str, list] = {}

        for book in self.books.values():
            for contact in book.details:
                person_city.setdefault(contact.city.title(), []).append(contact)
                person_state.setdefault(contact.state.title(), []).append(contact)

        try:
            choice = int(input("\nEnter (1)-City (2)-State: "))
        except ValueError:
            print("Invalid entry.")
            return

        mapping = person_city if choice == 1 else person_state if choice == 2 else None
        if mapping is None:
            print("Invalid choice")
            return

        for place, people in mapping.items():
            print(
                f"\n{place} ({len(people)} contact{'s' if len(people) != 1 else ''})"
            )
            if not count_only:
                for person in people:
                    print(person)

    def count_by_city_or_state(self) -> None:
        self.view_by_city_or_state(count_only=True)
