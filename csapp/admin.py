from django.contrib import admin
from csapp.models import Course, CourseRating, UserProfile 

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('dateTime',)

admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile)
admin.site.register(CourseRating, ReviewAdmin)


    
