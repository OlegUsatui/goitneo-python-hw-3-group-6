from address_book import AddressBook, Record


class NotEnoughValuesToUnpack(Exception):
    pass


class DictAreEmpty(Exception):
    pass


class ContactIsNotExists(Exception):
    pass


class NotEnoughName(Exception):
    pass


class PhoneIsExist(Exception):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotEnoughName:
            return "Give me name please."
        except NotEnoughValuesToUnpack:
            return "Give me name and phone please."
        except ContactIsNotExists:
            return 'Contact with this name not found.'
        except DictAreEmpty:
            return 'No contacts here yet.'
        except PhoneIsExist:
            return 'Phone is exist.'
        except ValueError as err:
            return err

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise NotEnoughValuesToUnpack

    name, phone = args
    normalized_name = name.capitalize()

    if normalized_name in book:
        return "A contact with the same name exists. Please enter a different contact name."

    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)

    return "Contact added."


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 2:
        raise NotEnoughValuesToUnpack

    name, phone = args

    record: Record = book.find(name)

    if record is None:
        raise ContactIsNotExists

    exist_phone = record.find_phone(phone)

    if exist_phone is None:
        record.change_phone(phone)
    else:
        raise PhoneIsExist

    return "Contact changed."


@input_error
def get_phone_number(args, book: AddressBook):
    if len(args) < 1:
        raise NotEnoughName

    if len(book) == 0:
        raise DictAreEmpty

    name, = args

    record: Record = book.find(name)

    if record is None:
        raise ContactIsNotExists

    phones = record.get_phones()

    return phones


@input_error
def get_all_contacts(book: AddressBook):
    if len(book) == 0:
        raise DictAreEmpty

    text = ''

    for name, number in book.items():
        text += f'{name}: {number}\n'
    return text


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise NotEnoughName

    if len(book) == 0:
        raise DictAreEmpty

    name, birthday = args

    record: Record = book.find(name)

    if record is None:
        raise ContactIsNotExists

    record.add_birthday(birthday)

    return 'Birthday added.'


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise NotEnoughName

    if len(book) == 0:
        raise DictAreEmpty

    name, = args

    record: Record = book.find(name)

    if record is None:
        raise ContactIsNotExists

    birthday = record.get_birthday()

    return birthday


@input_error
def find_birthdays_next_week(book: AddressBook):
    if len(book) == 0:
        raise DictAreEmpty

    return book.get_birthdays_per_week()


@input_error
def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        try:
            command, *args = parse_input(user_input)
        except ValueError:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone_number(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(find_birthdays_next_week(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
