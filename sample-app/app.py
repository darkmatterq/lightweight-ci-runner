import re


def is_even(num):
    if num % 2 == 0:
        return f"'{num}' is even"
    return f"'{num}' is odd"


def is_prime(num):
    if num <= 1:
        return False
    count = 0
    point_end = int(num ** 0.5) + 1
    for i in range(2, point_end):
        if num % i == 0:
            count += 1
        if count > 0:
            return False
    return True


def format_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(pattern, email):
        return True
    return False


if __name__ == "__main__":
    num = 8
    if is_prime(num):
        print(num, "is Prime\n")
    else:
        print(num, "isn't Prime\n")

    print(is_even(num))

    list_email = [
        "quan.ledinh@gmail.com",
        "le dinh quan@uit.edu.vn",
        "quan@gmail",
        "kdq#2006@yahoo.com",
        "nguyen..van.a@gmail.com",
    ]

    for mail in list_email:
        if format_email(mail):
            print(f"'{mail}' ---> Correct✅\n")
        else:
            print(f"'{mail}' ---> Incorrect❌\n")


