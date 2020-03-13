from django.urls import path
from csapp import views

app_name = 'csapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.about, name='about'),
    path('undergraduate/', views.undergraduate, name='undergraduate'),
    path('postgraduate/', views.postgraduate, name='postgraduate'),
    path('days/', views.about, name='days'),
    path('postgraduate/<slug:course_name_slug>', views.postgraduate_course, name='course')
]
    
