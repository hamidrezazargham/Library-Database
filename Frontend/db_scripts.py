import requests
from data import BASE_URL


def get_user_ids() -> list:
    response = requests.get(url=BASE_URL + "users/")
    users_ids = response.json()['users']
    return users_ids


def add_member(member: dict):
    res = requests.post(url=BASE_URL + "add-member/", data=member)
    return res


def add_employee(employee: dict):
    res = requests.post(url=BASE_URL + "add-employee/", data=employee)
    return res

def add_author(author: dict):
    res = requests.post(url=BASE_URL + "add-author/", data=author)
    return res


def add_book(book: dict):
    res = requests.post(url=BASE_URL + "add-book/", data=book)
    return res

def borrow(borrow: dict):
    res = requests.post(url=BASE_URL + "borrow/", data=borrow)
    return res

def return_book(borrow: dict):
    res = requests.post(url=BASE_URL + "return/", data=borrow)
    return res

def delete_book(book: dict):
    res = requests.post(url=BASE_URL + "delete-book/", data=book)
    return res

def search_book(title):
    res = requests.get(url=BASE_URL + f"search-book/{title}")
    return res

def members_log():
    response = requests.get(url=BASE_URL + "members-log/")
    return response.json()

def employees_log():
    response = requests.get(url=BASE_URL + "employees-log/")
    return response.json()

def authors_log():
    response = requests.get(url=BASE_URL + "authors-log/")
    return response.json()

def books_log():
    response = requests.get(url=BASE_URL + "books-log/")
    return response.json()

def borrows_log():
    response = requests.get(url=BASE_URL + "borrows-log/")
    return response.json()

def returns_log():
    response = requests.get(url=BASE_URL + "returns-log/")
    return response.json()
