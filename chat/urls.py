from django.urls import path

from chat import views

urlpatterns = [
    path('', views.chat, name='index'),
    path('messages/', views.messages, name='messages'),
]
