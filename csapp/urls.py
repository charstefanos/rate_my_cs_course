from django.urls import path
from csapp import views

app_name = 'csapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.about, name='about'),
    path('undergraduate/', views.undergraduate, name='undergraduate'),
    path('postgraduate/', views.postgraduate, name='postgraduate'),
    path('opendays/', views.opendays, name='opendays'),
    path('postgraduate/<slug:course_name_slug>', views.course, name='course'),
    path('undergraduate/<slug:course_name_slug>', views.course, name='course'),
    path('profile/', views.profile, name='profile'),
    path('profile/delete', views.delete_profile, name='delete_profile'),
    path('search/', views.search, name='search'),
    path('postgraduate/<slug:course_name_slug>/write_review', views.write_review, name='write_review'),
    path('undergraduate/<slug:course_name_slug>/write_review', views.write_review, name='write_review'),
    path('my_reviews', views.my_reviews, name='my_reviews'),
    path('my_reviews/<slug:course_name_slug>/delete_review', views.delete_review, name='delete_review'),
    
]
    
