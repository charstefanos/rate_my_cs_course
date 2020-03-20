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
    path('postgraduate/<slug:course_name_slug>', views.postgraduate_course, name='course'),
    #@Stefanos: I removed the year parameter as it wasnt running but i will try and figure it
    # out later
    path('undergraduate/<slug:course_name_slug>', views.undergraduate_course, name='course'),
    path('profile/', views.profile, name='profile'),
    path('profile/delete', views.delete_profile, name='delete_profile'),
    path('search/', views.search, name='search'),
    path('postgraduate/<slug:course_name_slug>/write_review', views.write_review, name='write_review'),
    path('undergraduate/<slug:course_name_slug>/write_review', views.write_review, name='write_review'),
    path('profile/my_reviews', views.my_reviews, name='my_reviews'),
]
    
