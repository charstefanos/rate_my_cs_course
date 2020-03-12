from django.contrib import admin
from csapp.models import Course, UserProfile, CourseRating

admin.site.register(Course)
admin.site.register(CourseRating)
admin.site.register(UserProfile)
