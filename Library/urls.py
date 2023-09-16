from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    #URLs after login
    
    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("view_members/", views.view_members, name="view_members"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("member_issued_books/", views.member_issued_books, name="member_issued_books"),
    path("profile/", views.profile, name="profile"),

    #URLs for login

    path("member_registration/", views.member_registration, name="member_registration"),
    path("member_login/", views.member_login, name="member_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),

    #Delete or Update data if needed
    
    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_member/<int:myid>/", views.delete_member, name="delete_member"),
    path("edit_book/<int:myid>/", views.edit_book, name="edit_book"),
    path("update/<int:myid>", views.update, name='update'),
]