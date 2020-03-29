from django import forms
from django.contrib.auth.models import User
from csapp.models import *
from django_starfield import Stars

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','password',)

        help_texts = {
            'username': None,
            }

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']

        help_texts = {
            'username': None,
            }

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','email','picture','current_student','year_of_studies','courses','contact')
        
        labels = {
            'first_name': 'First name:',
            'last_name' : 'Surname:',
            'email' : 'Email:',
            'picture' : 'Picture:',
            'current_student' : 'Are you currently a student at University of Glasgow?',
            'year_of_studies' : 'What year are you currently in?',
            'courses' : 'What courses did you take?',
            'contact' : 'Would you like your username and email to be visible for others to see?',
            }

        widgets = {
            'courses' : forms.SelectMultiple(attrs={'class' : 'selectCourses'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['courses'].queryset = Course.objects.none()

        if 'year_of_studies' in self.data:
            try:
                yearOfStudies = int(self.data.get('year_of_studies'))
                print(yearOfStudies)
                self.fields['courses'].queryset = Course.objects.filter(year_in_university__lte = yearOfStudies).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            if(self.instance.year_of_studies != None):
                self.fields['courses'].queryset = Course.objects.filter(year_in_university__lte = self.instance.year_of_studies).order_by('name')

#This is some testing for the reviews but havent been tested yet
class ReviewForm(forms.ModelForm):
    overall_rating = forms.IntegerField(widget=Stars)
    lecturer_rating = forms.IntegerField(widget=Stars)
    engagement = forms.IntegerField(widget=Stars)
    informative = forms.IntegerField(widget=Stars)
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'reviewComment','placeholder': 'Leave a comment for this course (optional). .'}))

    class Meta:
        model = CourseRating
        # include all fields in the form.
        exclude = ("student", "course",)

class ReviewDeleteForm(forms.ModelForm):
    class Meta:
        model = CourseRating
        fields = []
    






    

       

        
            
