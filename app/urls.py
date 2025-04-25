from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("blogs", views.blogs, name="blogs"),
    path("blog/<str:pk>", views.blog, name="blog"),
    path("blog-edit/<str:pk>", views.edit_blog, name="blog-edit"),
    path("blog-delete/<str:pk>", views.delete_blog, name="blog-delete"),
    path("blog_form", views.create_blog, name="blog_form"),
    path("login", views.user_login, name="login"),
    path("register", views.user_register, name="register"),
    path("logout", views.user_logout, name="logout"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("profile-edit/", views.edit_profile, name="profile-edit"),
    path("private-chat/<str:pk>", views.private_chat, name="private-chat"),
    path("my-chats", views.my_chats, name="my-chats"),
    path("public-chat", views.public_chat, name="public-chat"),
    path("poker-rooms", views.poker_rooms, name="poker-rooms"),
    path("poker-form", views.create_poker, name="poker-form"),
    path("poker-room/<str:pk>", views.poker_room, name="poker-room"),
    path("join-poker/<str:pk>", views.join_poker, name="join-poker"),
    path("leave-poker/<str:pk>", views.leave_poker, name="leave-poker"),

    path("bridge", views.bridge, name="bridge"),
]