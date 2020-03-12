from django.shortcuts import render
from django.http import HttpResponse
from csapp.forms import UserForm, UserProfileForm, CurrentStudentForm

def home(request):
    return render(request, 'csapp/home.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        current_student_form = CurrentStudentForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and current_student_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            student = current_student_form.save()
            student.user = user
            student.save()
            
            registered = True
        else:
            print(user_form.errors, profile_form.errors, current_student_form.erros)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        current_student_form = CurrentStudentForm()

    return render(request,
                  'csapp/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'current_student_form' : current_student_form,
                             'registered': registered})
    
