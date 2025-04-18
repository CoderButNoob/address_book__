import pytest
from faker import Faker
from details import Details
from address_book import AddressBook
from address_book_system import AddressBookSystem

fake = Faker("en_IN")

india_state_and_city = {
    "Maharashtra": ["Mumbai", "Pune"],
    "West Bengal": ["Kolkata", "Durgapur"],
    "Karnataka": ["Bangalore", "Mysore"],
    "Delhi": ["New Delhi"],
    "Tamil Nadu": ["Chennai", "Coimbatore"],
    "Uttar Pradesh": ["Lucknow", "Kanpur"]
}

def generate_fake_contact():
    state = fake.random_element(elements=list(india_state_and_city.keys()))
    city = fake.random_element(elements=india_state_and_city[state])
    return{
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": fake.street_address(),
        "city": city,
        "state": state,
        "zip_code": fake.postcode()[:6],
        "phone": f"+91 {fake.random_number(digits=10 , fix_len=True)}",
        "email": fake.email()
    }

def test_fake_valid():
    fake_contact = generate_fake_contact()
    contact = Details(**fake_contact)
    assert contact.first_name == fake_contact["first_name"]
    assert contact.last_name == fake_contact["last_name"]
    assert contact.city == fake_contact["city"]
    assert contact.state == fake_contact["state"]
    assert contact.zip_code.isdigit()
    assert contact.phone.startswith("+91")
    assert "@"  in contact.email

def test_fake_add_contact():
    book = AddressBook()
    for _ in range(10):
        contact = Details(**generate_fake_contact())
        book.details.append(contact)
    
    assert len(book.details) == 10

# def test_group_by_city():
#     book = AddressBook()
#     for _ in range(10):
#         conatct = Details(**generate_fake_contact())
#         book.details.append(conatct)
    
#     city = {}
#     for contact in book.details:
#         city.setdefault
        
    
