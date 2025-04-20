import json
from details import Details

class AddressBookFileManagerJSON:

    @staticmethod
    def write_json(details, file="address_book.json"):
        with open(file, 'w') as f:
            json.dump([contact.model_dump() for contact in details], f, indent=4)
        print(f"Written to JSON file: {file}")

    @staticmethod
    def read_json(file="address_book.json"):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                return [Details(**item) for item in data]
        except FileNotFoundError:
            print("JSON file not found")
            return []
