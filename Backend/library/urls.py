from django.http import JsonResponse
from django.urls import path
import psycopg2
from . import views


urlpatterns = [
  path("add-member/", views.add_member, name="add member"),
  path("add-employee/", views.add_employee, name="add employee"),
  path("add-book/", views.add_book, name="add book"),
  path("add-author/", views.add_author, name="add author"),
  path("users/", views.get_users, name="users"),
  path("borrow/", views.borrow, name="borrow"),
  path("return/", views.return_book, name="return"),
  path("delete-book/", views.delete_book, name="delete book"),
  path("search-book/<str:title>/", views.search_book, name="search book"),
  path("authors-log/", views.authors_log, name="authors log"),
  path("books-log/", views.books_log, name="books log"),
  path("members-log/", views.members_log, name="members log"),
  path("employees-log/", views.employees_log, name="employees log"),
  path("borrows-log/", views.borrows_log, name="borrows log"),
  path("returns-log/", views.returns_log, name="returns log"),
]