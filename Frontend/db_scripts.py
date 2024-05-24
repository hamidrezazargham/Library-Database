import requests
import json
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