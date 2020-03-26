from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


#The list of available options organised into two groups. Contains tuples (value, human-readable name).
YEAR_IN_UNI_CHOICES = (
    (1, 'Undergraduate (year 1)'),
    (2, 'Undergraduate (year 2)'),
    (3, 'Undergraduate (year 3)'),
    (4, 'Undergraduate (year 4)'),
    (5, 'Postgraduate'),
    )

class Course(models.Model):
#We have specified 30 for length of the name, but I will leave it 128 for now - can be changed.
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1000)
    year_in_university = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
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
    email = models.EmailField(max_length=30, unique=True)
    picture = models.ImageField(default='default.jpg', upload_to='profile_images')
    current_student = models.BooleanField(default = False)
    
    year_of_studies = models.IntegerField(
        choices=YEAR_IN_UNI_CHOICES,
        null = True,
        blank = True,
    )
    courses = models.ManyToManyField(Course, blank = True)
    contact = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        
    def __str__(self):
        return self.user.username
        
    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
            
#Implemented rating as integers - to be conveted from the number of stars a user has chosen.
class CourseRating(models.Model):
    #two foreign keys - for the student and the course (one-to-many relationships)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # changed the values of the rating so they can only choose between 1 and 5
    overall_rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    lecturer_rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    engagement = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    informative = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.CharField(max_length = 250, blank = True)
    dateTime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.overall_rating)

    class Meta:
        verbose_name = 'Course Rating'
        verbose_name_plural = 'Course Ratings'
