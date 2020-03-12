from django import forms
from django.contrib.auth.models import User
from csapp.models import UserProfile
from csapp.models import UofGStudent

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
        fields = ('first_name','last_name','email','picture','current_student')
        
        labels = {
            'first_name': 'Fist name',
            'last_name' : 'Surname',
            'email' : 'Email',
            'current_student' : 'Are you currently a student?',
            }

        widgets = {
            'current_student' : forms.RadioSelect(choices = TRUE_FALSE_CHOICES),
            }

#We should use javascript or ajax to blank out this section of the answer to current student is no
class CurrentStudentForm(forms.ModelForm):
    class Meta:
        model = UofGStudent
        fields = ('year_of_studies','courses','contact')

        labels = {
            'year_of_studies' : 'What year are you currently on?',
            'courses' : 'What courses did you take?',
            'contact' : 'Would you like your name and email to be visible for others to see?',
            }

        widgets = {
            'contact' : forms.RadioSelect(choices = TRUE_FALSE_CHOICES),
             }

    

       

        
            
