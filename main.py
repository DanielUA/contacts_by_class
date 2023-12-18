from collections import UserDict

class Field:
    def __init__(self, value, name):
        self.value = value
        self.name = name

class Name(Field):
    def validation(self, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Number must be 10 digits.")

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid phone number.")
        super().__init__(value, "phone")

    def is_valid(self, number):
        return len(number) == 10 and number.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name, "name")
        self.phones = []

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                if phone.is_valid(new_number):
                    phone.value = new_number
                else:
                    raise ValueError(f"Invalid phone number: {new_number}")
                return
        raise ValueError(f"Phone number '{old_number}' does not exist for editing.")

    def find_phone(self, phone_number):
        return next((phone for phone in self.phones if phone.value == phone_number), None)

    def __str__(self):
        phones_str = '; '.join(str(phone.value) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]



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
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
book.delete("Jane")