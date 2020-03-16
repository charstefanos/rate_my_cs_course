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

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

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
            #'current_student' : forms.RadioSelect(choices = TRUE_FALSE_CHOICES),
            #'contact' : forms.RadioSelect(choices = TRUE_FALSE_CHOICES),
            'courses' : forms.CheckboxSelectMultiple(),
            }
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username']

        help_texts = {
            'username': None,
            }
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','email','picture','current_student','year_of_studies','courses','contact')
        
        labels = {
            'first_name': 'First name',
            'last_name' : 'Surname',
            'email' : 'Email',
            'current_student' : 'Are you currently a student at University of Glasgow?',
            'year_of_studies' : 'What year are you currently in?',
            'courses' : 'What courses did you take',
            'contact' : 'Would you like your name and email to be visible for others to see?',
            }

        widgets = {
            'current_student' : forms.RadioSelect(choices = TRUE_FALSE_CHOICES),
            'contact' : forms.RadioSelect(choices = TRUE_FALSE_CHOICES),
            'courses' : forms.CheckboxSelectMultiple(),
            }

#This is some testing for the reviews but havent been tested yet
class ReviewForm(forms.ModelForm):
    CHOICES = ((1, 'Terrible'), (2, 'Bad'), (3, 'Average'), (4, 'Good'), (5, 'Excellent'))
    overall_rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    lecturer_rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    engagement = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    informative = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    waiting_time = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    comment = forms.CharField(required=False)

    class Meta:
        model = CourseRating
        # include all fields in the form.
        exclude = ("student", "course",)






    

       

        
            
