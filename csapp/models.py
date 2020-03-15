from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

#The list of available options organised into two groups. Contains tuples (value, human-readable name).
YEAR_IN_UNI_CHOICES = (
    ('Undergraduate', (
            ('UNDERGRAD_1YEAR', 'Undergraduate (year 1)'),
            ('UNDERGRAD_2YEAR', 'Undergraduate (year 2)'),
            ('UNDERGRAD_3YEAR', 'Undergraduate (year 3)'),
            ('UNDERGRAD_4YEAR', 'Undergraduate (year 4)'),
        )
    ),
    ('Postgraduate', (
            ('POSTGRAD', 'Postgraduate'),
        )
    ),
    )

class Course(models.Model):
#We have specified 30 for length of the name, but I will leave it 128 for now - can be changed.
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1000)
    year_in_university = models.IntegerField(default=0)
    
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
        
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    picture = models.ImageField(default='default.jpg', upload_to='profile_images')
    current_student = models.BooleanField(default = False)
    
    year_of_studies = models.CharField(
        max_length=32,
        choices=YEAR_IN_UNI_CHOICES,
        null = True,
        blank = True
    )
    courses = models.ManyToManyField(Course, blank = True)
    contact = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        
    def __str__(self):
        return self.user.username
    
#Implemented rating as integers - to be conveted from the number of stars a user has chosen.
class CourseRating(models.Model):
    #two foreign keys - for the student and the course (one-to-many relationships)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    overall_rating = models.IntegerField(default=0)
    lecturer_rating = models.IntegerField(default=0)
    engagement = models.IntegerField(default=0)
    informative = models.IntegerField(default=0)
    comment = models.CharField(max_length = 250, blank = True)
    def __str__(self):
        return self.overall_rating

    class Meta:
        verbose_name = 'Course Rating'
        verbose_name_plural = 'Course Ratings'
        
       
