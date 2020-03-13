from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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
            print(user_form.errors, profile_form.errors, current_student_form.errors)
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
                             
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('csapp:home'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'csapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('csapp:home'))


