from django import forms
from django.contrib.auth.models import User
from csapp.models import UserProfile, Course

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






    

       

        
            
