from django.urls import path
from csapp import views

app_name = 'csapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
    
