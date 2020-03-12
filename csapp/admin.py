from django.contrib import admin
from csapp.models import Course, UofGStudent, NonStudent, CourseRating

admin.site.register(Course)
admin.site.register(CourseRating)
admin.site.register(UofGStudent)
admin.site.register(NonStudent)
