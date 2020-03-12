from django.db import models
from django.contrib.auth.models import User
from star_ratings.models import Rating

class Course(models.Model):
#We have specified 30 for length of the name, but I will leave it 128 for now - can be changed.
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=200)
    #The list of available options organised into two groups. Contains tuples (value, human-readable name).
    YEAR_IN_UNI_CHOICES = (
    ('Undergraduate', (
            ('UNDERGRAD_1YEAR', 'Undergraduate (year 1)'),
            ('UNDERGRAD_2YEAR', 'Undergraduate (year 2)'),
            ('UNDERGRAD_3YEAR', 'Undergraduate (year 3)'),
            ('UNDERGRAD_1YEAR', 'Undergraduate (year 4)'),
        )
    ),
    ('Postgraduate', (
            ('POSTGRAD', 'Postgraduate'),
        )
    ),
    )
    year_in_uni = models.CharField(
        max_length=32,
        choices=YEAR_IN_UNI_CHOICES,
    )
    def __str__(self):
        return self.name

#installed: pip install django-star-ratings. Added it in installed apps in settings.py and in the urls.py. 
# However, needs to be checked exactly how to be used. Full documentation at https://django-star-ratings.readthedocs.io/en/latest/?badge=latest/#
# If needed, can be uninstalled and removed completely.
class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    overall_rating = Rating
    lecturer_rating = Rating
    engagement = Rating
    informative = Rating
    comment = models.CharField(max_length = 250, blank = True)
    def __str__(self):
        return self.overall_rating

        
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    current_student = models.BooleanField()
    def __str__(self):
        return self.user.username
        
