import json
from faker import Faker
import random
import re

fake = Faker()

# Regex patterns for validation
phone_pattern = r"^\+91\s\d{10}$"  # Indian phone number format: +91 1234567890
zip_pattern = r"^\d{6}$"  # 6 digit zip code
name_pattern = r"^[A-Z][a-z]*$"  # Name starts with a capital letter followed by lowercase letters

def generate_json(filename="contacts.json", total_records=100000, max_address_book_id=4):
    contacts = []

    for _ in range(total_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()
        zip_code = fake.zipcode()

        # Validate and adjust first name and last name
        if not re.match(name_pattern, first_name):
            first_name = first_name.capitalize()  # Ensure first letter is capitalized
        if not re.match(name_pattern, last_name):
            last_name = last_name.capitalize()  # Ensure first letter is capitalized

        # Validate phone number format
        if not re.match(phone_pattern, phone):
            phone = "+91 " + "".join([str(random.randint(0, 9)) for _ in range(10)])  

        # Validate zip code format
        if not re.match(zip_pattern, zip_code):
            zip_code = "".join([str(random.randint(0, 9)) for _ in range(6)])  

        contact = {
            "address_book_id": random.randint(1, max_address_book_id),
            "first_name": first_name,
            "last_name": last_name,
            "email": fake.email(),
            "phone": phone,
            "address": fake.address().replace("\n", " "),
            "city": fake.city(),
            "state": fake.state(),
            "zip": zip_code
        }
        contacts.append(contact)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=2)

    print(f"{total_records} contacts generated into {filename}!")

if __name__ == "__main__":
    generate_json()
