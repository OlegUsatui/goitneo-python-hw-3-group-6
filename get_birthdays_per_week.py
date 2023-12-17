from collections import defaultdict
from datetime import datetime

today = datetime.today().date()


def get_birthdays_per_week(users):
    birthdays = defaultdict(list)

    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        if 0 <= delta_days < 7:
            day_of_week = birthday_this_year.strftime('%A')
            birthdays[day_of_week].append(name)
    str = ''
    for day, names in birthdays.items():
        str += f"{day}: {', '.join(names)}\n"
    return str


if __name__ == "__main__":
    # TESTS
    users = [
        {"name": "Bill Gates", "birthday": datetime(today.year, today.month, today.day + 2)},
        {"name": "Steve Jobs", "birthday": datetime(today.year, today.month, today.day + 3)},
        {"name": "Jan Koum", "birthday": datetime(today.year, today.month, today.day + 4)}
    ]

    print(get_birthdays_per_week(users))
