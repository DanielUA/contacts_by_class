from collections import UserDict
from datetime import date, datetime
import os
import pickle


class Field():
    def __init__(self, value):
        if not self.valid(value):
            raise ValueError("Incorrect value")
        self.__value = value
    
    def valid(self, value):
        return True
 
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.valid(value):
            raise ValueError("Incorrect value")
        self.__value = value

class Name(Field):
    def valid(self, value):
        return value.isalpha()


class Phone(Field):
    def valid(self, value):
        if not (len(value) == 10 and value.isdigit()):
            return False
        return True


class Birthday(Field):
    def valid(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False 


class Record:
    def __init__(self, name, birthday=None, file=None):
        self.name = Name(name)
        self.file = file if file is not None else None
        self.phones = []
        self.birthday = Birthday(birthday) if birthday is not None else None

    def days_to_birthday(self):
        if self.birthday is None:
            return "no data of birthday"
        day_now = date.today()
        str_date = self.birthday.value
        try:
            birth_update = datetime.strptime(str_date, "%d.%m.%Y")
            year_birthday = birth_update.replace(year=day_now.year)
            days_until_birthday = (year_birthday - day_now).days
            if days_until_birthday < 0:
                year_birthday = birth_update.replace(year=day_now.year + 1)
                days_until_birthday = (year_birthday - day_now).days
            return days_until_birthday
        except ValueError:
            return "Incorrect date format"

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                phone.valid(new_number)
                return 
        raise ValueError(f"Invalid phone number: {old_number}")

    def find_phone(self, phone_number):
        return next((phone for phone in self.phones if phone.value == phone_number), None)
    
    def find_user_by_phone_name(self, query):
        query = query.lower()
        if query.isdigit():
            for phone in self.phones:
                if query in phone.value:
                    return str(self)
        elif query.isalpha():
            if query in self.name.value.lower():
                return str(self)
        return None

    def __str__(self):
        phones_str = '; '.join(str(phone.value) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def iterator(self, n):
        values = list(self.data.values())
        for i in range(0, len(values), n):
            yield values[i:i + n]

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def save_address_book(self):
        if self.file:
            with open(self.file, "wb") as fh:
                pickle.dump(self, fh)
            print("Address book saved successfully.")

    def load_address_book(self):
        if self.file and os.path.exists(self.file):
            with open(self.file, "rb") as fh:
                content = pickle.load(fh)
                print("Address book loaded successfully.")
                return content
        else:
            print(f"File '{self.file}' not found.")
            return None

    def search(self, query):
        result = []
        for record in self.data.values():
            found_user = record.find_user_by_phone_name(query)
            if found_user:
                result.append(found_user)
        return result

    



    # Створення нової адресної книги
book = AddressBook()

    # Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
book.add_record(john_record)

    # Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

    # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

    # Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")

    # Видалення запису Jane
book.delete("Jane")

# Збереження адресної книги на диск
book.file = "address_book.pkl"
book.save_address_book()

# Відновлення адресної книги з диска
restored_book = AddressBook()
restored_book.file = "address_book.pkl"
restored_book.load_address_book()