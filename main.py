from collections import UserDict
import re

class Field:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __str__(self):
        return str(self.value)

class Name(Field):
    def validation(self, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Number must be 10 digits.")
/home/daniel/go-it/contact_boocd
class Phone(Field):
    def __init__(self, value, name):
        super().__init__(value, name)
        self.validation(value)

    def validation(self, number):
        if not len(number) == 10 and number.isdigit() and number[0] == "0":
        # if not re.match(r'^\d{10}$', number):
            raise ValueError("Number must be 10 digits.")

class Record:
    def __init__(self, name):
        self.name = Name(name, "name")
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number, "phone")
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.validation(new_number)
                phone.value = new_number
                break
        else:
            raise ValueError(f"Phone number '{old_number}' does not exist for editing.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

# Приклад використання:
address_book = AddressBook()

record1 = Record("John Doe")
record1.add_phone("1234567890")
record1.add_phone("0505563421")

record2 = Record("Jane Doe")
record2.add_phone("5555555555")

address_book.add_record(record1)
address_book.add_record(record2)

# Пошук записів за іменем
found_record = address_book.find("John Doe")
if found_record:
    print(found_record)
else:
    print("Record not found")

# Видалення записів за іменем
address_book.delete("John Doe")

# Пошук записів після видалення
found_record = address_book.find("John Doe")
if found_record:
    print(found_record)
else:
    print("Record not found")
