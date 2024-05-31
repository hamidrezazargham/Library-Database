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
  path("search-book/<str:title>/", views.search_book, name="search book")

  #  """ path("borrow/", views.borrow, name="borrow"),
  #   path("return/", views.return, name="return"),
  #   path("deletemember/", views.delete_member, name="deletemember"),
  #   path("deletebook/", views.delete_book, name="deletebook")

  #   path("editjob/<str:pk>", views.edit_job, name="editjob"),
  #   path("add-book/", views.add_book)"""
]