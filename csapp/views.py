from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from csapp.forms import UserForm, UserProfileForm
from csapp.models import Course
from django.http import Http404 


def home(request):
    return render(request, 'csapp/home.html')

def undergraduate(request):
    return render(request, 'csapp/undergraduate.html')

def postgraduate(request):
    return render(request, 'csapp/postgraduate.html')

def about(request):
    return render(request, 'csapp/about.html')

def opendays(request):
    return render(request, 'csapp/opendays.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            profile_form.save_m2m()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request,
                  'csapp/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
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
    
def postgraduate_course(request, course_name_slug):
    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        raise Http404("Course does not exist") 
    return render(request, 'csapp/course.html', {'course':course})
    
    
def undergraduate_course(request, course_name_slug, year):
    try:
        course = Course.objects.get(slug=course_name_slug)
        #check if course has right corresponding year in URL
        if course.year_in_university != year:
            raise Http404("Wrong year") 
    except Course.DoesNotExist:
        raise Http404("Course does not exist") 
    return render(request, 'csapp/course.html', {'course':course})
    
    
@login_required    
def profile(request):
    return render(request, 'csapp/profile.html')
    

