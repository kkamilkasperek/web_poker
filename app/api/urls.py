from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('blogs/', views.get_blogs),
    path('blogs/<str:pk>/', views.get_blog),
    path('chats/<str:chat_id>/messages/', views.get_new_messages, name="get_new_messages"),
]