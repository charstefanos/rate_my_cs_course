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

#This is temporary, just trying to see if it will work.
All_Courses = (
    ('Undergraduate', (
        ('LEVEL_1', '1CT INTRODUCTION TO COMPUTATIONAL THINKING COMPSCI1016',
                   '1S SYSTEMS COMPSCI1018',
                   '1F COMPUTING FUNDAMENTALS COMPSCI1006',
                    '1P (STANDARD ROUTE) COMPSCI1001',
                    '1P (HALF COURSE) COMPSCI1005',
                    '1PX (ALTERNATE ROUTE) COMPSCI1017',
                    'FOUNDATIONS OF PROFESSIONAL SOFTWARE ENGINEERING COMPSCI1019',
                    'HOW TO LEARN A NEW LANGUAGE COMPSCI1020',
                    'PRACTICAL ALGORITHMS COMPSCI1021',
                    'SPATIAL SKILLS TRAINING 1 COMPSCI1026',
                    'TESTING AND SOFTWARE IMPROVEMENT COMPSCI1022',
                    'WEB APPLICATION SYSTEMS COMPSCI1023',
                    'WORKPLACE ASSESSMENT YEAR 1 COMPSCI1024')

    ))
)

class Course(models.Model):
#We have specified 30 for length of the name, but I will leave it 128 for now - can be changed.
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=200)
    year_in_university = models.CharField(
        max_length=32,
        choices=YEAR_IN_UNI_CHOICES,
    )
    
    
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
    email = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    current_student = models.BooleanField()
    def __str__(self):
        return self.user.username
    class Meta:
        abstract = True

#subclasses of the abstract class
class UofGStudent(UserProfile):
    #added year of studies to be able to filter the courses they need to choose from
    year_of_studies = models.CharField(
        max_length=32,
        choices=YEAR_IN_UNI_CHOICES,
    )
    courses = models.ManyToManyField(Course)
    contact = models.BooleanField()

    class Meta:
        verbose_name = 'UofG Student'
        verbose_name_plural = 'Uofg Students'

class NonStudent(UserProfile):

    class Meta:
        verbose_name = 'Non student'
        verbose_name_plural = 'Non Students'
        
    pass



#Implemented rating as integers - to be conveted from the number of stars a user has chosen.
class CourseRating(models.Model):
    #two foreign keys - for the student and the course (one-to-many relationships)
    student = models.ForeignKey(UofGStudent, on_delete=models.CASCADE)
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
        
       
