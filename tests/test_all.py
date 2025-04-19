import pytest
from faker import Faker
from details import Details
from address_book import AddressBook
from address_book_system import AddressBookSystem,AddressBookSearch

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

@pytest.fixture
def sample_contacts():
    return [Details(**generate_fake_contact()) for _ in range(10)]

# def test_fake_valid():
#     fake_contact = generate_fake_contact()
#     contact = Details(**fake_contact)
#     assert contact.first_name == fake_contact["first_name"]
#     assert contact.last_name == fake_contact["last_name"]
#     assert contact.city == fake_contact["city"]
#     assert contact.state == fake_contact["state"]
#     assert contact.zip_code.isdigit()
#     assert contact.phone.startswith("+91")
#     assert "@"  in contact.email

def test_fake_add_contact(sample_contacts):
    book = AddressBook()
    for contact in sample_contacts:
        book.details.append(contact)    
    assert len(book.details)==10

def test_edit(sample_contacts):
    book = AddressBook()
    book.details.append(sample_contacts[0])
    f_name = book.details[0].first_name 
    book.details[0].first_name = "Anything"
    assert book.details[0].first_name != f_name

def test_delete(sample_contacts):
    book = AddressBook()
    book.details.append(sample_contacts[0])
    previous_len = len(book.details)
    book.details.remove(sample_contacts[0])
    assert len(book.details) == previous_len - 1

def test_multiple_addressbook(sample_contacts):
    search = AddressBookSearch()
    search.books["Friends"] = AddressBook()
    search.books["Family"] = AddressBook()
    assert 'Friends' in search.books and 'Family' in search.books

def test_no_duplicate(sample_contacts):
    book = AddressBook()
    contact = sample_contacts[0]
    book.details.append(contact)
    duplicates = [c for c in book.details if c.first_name == contact.first_name and c.last_name == contact.last_name]
    assert len(duplicates) == 1


def test_group_by_city(sample_contacts):
    book = AddressBook()
    book.details.extend(sample_contacts)
    city_map = {}
    for contact in book.details:
        city_map.setdefault(contact.city, []).append(contact)
    assert isinstance(city_map,dict)

def test_group_by_state(sample_contacts):
    book = AddressBook()
    book.details.extend(sample_contacts)
    state_map = {}
    for contact in book.details:
        state_map.setdefault(contact.state, []).append(contact)
    assert isinstance(state_map,dict)

def test_count_by_city(sample_contacts):
    city_count = {}
    for c in sample_contacts:
        city_count[c.city] = city_count.get(c.city,0)+1
    assert sum(city_count.values()) == len(sample_contacts)

def test_count_by_state(sample_contacts):
    state_count = {}
    for c in sample_contacts:
        state_count[c.state] = state_count.get(c.state,0)+1
    assert sum(state_count.values()) == len(sample_contacts)

def test_sort(sample_contacts):
    book = AddressBook()
    book.details.extend(sample_contacts)
    book.details.sort(key = lambda c : c.first_name.lower())
    sorted_name = [c.first_name for c in book.details]
    assert sorted_name == sorted(sorted_name, key=str.lower)





# def test_group_by_city():
#     book = AddressBook()
#     for _ in range(10):
#         conatct = Details(**generate_fake_contact())
#         book.details.append(conatct)
    
#     city_map = {}
#     for contact in book.details:
#         city_map.setdefault(contact.city, []).append(contact)
    
#     assert any(len(contacts)>1 for contacts in city_map.values())

# def test_group_by_state():
#     book = AddressBook()
#     for _ in range(10):
#         conatct = Details(**generate_fake_contact())
#         book.details.append(conatct)
    
#     state_map= {}
#     for contact in book.details:
#         state_map.setdefault(conatct.state, []).append(contact)
    
#     assert any(len(contacts)>1 for contacts in state_map.values())

# def test_group_city_state(monkeypatch , capsys):
#     system = AddressBook()
#     system.books[""]
        
    
