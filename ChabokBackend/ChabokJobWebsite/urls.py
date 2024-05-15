from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("home/", views.home_page, name="home"),
    path("jobs/<str:pk>/", views.view_job, name="viewjob"),
    path("profile/", views.profile, name="profile"),
    path("addjob/", views.create_job, name="createjob"),
    path("deletejob/<str:pk>", views.delete_job, name="deletejob"),
    path("editjob/<str:pk>", views.edit_job, name="editjob"),
    path("add-book/", views.add_book)
]