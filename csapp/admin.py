from django.contrib import admin
from csapp.models import Course, CourseRating, UserProfile 

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

class ReviewAdmin(admin.ModelAdmin):
    list_dispaly = ('course', 'username', 'comment')

admin.site.register(CourseRating)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile)
#admin.site.register(CourseRating, ReviewAdmin)


    
