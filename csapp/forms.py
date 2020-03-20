from django import forms
from django.contrib.auth.models import User
from csapp.models import *

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
            'contact' : 'Would you like your name and email to be visible for others to see?',
            }

        widgets = {
            'courses' : forms.SelectMultiple(),
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
    CHOICES = ((1, 'Terrible'), (2, 'Bad'), (3, 'Average'), (4, 'Good'), (5, 'Excellent'))
    overall_rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    lecturer_rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    engagement = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    informative = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    comment = forms.CharField(required=False)

    class Meta:
        model = CourseRating
        # include all fields in the form.
        exclude = ("student", "course",)






    

       

        
            
