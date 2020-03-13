from django.contrib import admin
from csapp.models import Course, UofGStudent, NonStudent, CourseRating

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

admin.site.register(CourseRating)
admin.site.register(UofGStudent)
admin.site.register(NonStudent)
admin.site.register(Course, CourseAdmin)


    
