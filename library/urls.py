from django.http import JsonResponse
from django.urls import path
import psycopg2
from . import views


urlpatterns = [
 path("addmember/", views.add_member, name="addmember"),
 path("addemployee/", views.add_employee, name="addemployee"),
 path("addbook/", views.add_book, name="addbook"),
 path("addauthor/", views.add_author, name="addauthor"),

  #  """ path("borrow/", views.borrow, name="borrow"),
  #   path("return/", views.return, name="return"),
  #   path("deletemember/", views.delete_member, name="deletemember"),
  #   path("deletebook/", views.delete_book, name="deletebook")

  #   path("editjob/<str:pk>", views.edit_job, name="editjob"),
  #   path("add-book/", views.add_book)"""
]