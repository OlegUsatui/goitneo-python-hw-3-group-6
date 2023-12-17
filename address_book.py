from collections import UserDict
from datetime import datetime
from get_birthdays_per_week import get_birthdays_per_week


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(f"Birthday {value} is invalid. Use DD.MM.YYYY format.")
        super().__init__(value)

    @staticmethod
    def validate(birthday_str):
        try:
            datetime.strptime(birthday_str, "%d.%m.%Y")
            return True
        except ValueError:
            return False


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(f"Phone number {value} is invalid. It must be 10 digits long.")
        super().__init__(value)

    @staticmethod
    def validate(phone):
        return phone.isdigit() and len(phone) == 10


class Record:
    def __init__(self, record_name):
        self.name = Name(record_name)
        self.phones = []
        self.birthday = None

    def get_phones(self):
        phones_str = ''
        if len(self.phones) < 1:
            return '[]'

        for phone in self.phones:
            phones_str += phone.value + '\n'
        return phones_str

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def change_phone(self, phone_number):
        self.phones = [Phone(phone_number)]

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def get_birthday(self):
        return self.birthday.value if self.birthday else "No birthday set"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record_item):
        record_name = record_item.name.value
        self.data[record_name] = record_item

    def find(self, record_name):
        return self.data.get(record_name)

    def delete(self, record_name):
        if record_name in self.data:
            del self.data[record_name]

    def get_birthdays_per_week(self):
        new_arr = []
        for record_name, record_item in self.data.items():
            new_arr.append({"name": record_name, "birthday": datetime.strptime(record_item.get_birthday(), "%d-%m-%Y")})
        return get_birthdays_per_week(new_arr)


if __name__ == "__main__":
    # TESTS
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")
