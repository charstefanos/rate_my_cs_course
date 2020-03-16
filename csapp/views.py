from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from csapp.forms import *
from csapp.models import *
from django.http import Http404 


def home(request):
    context_dict = {}
    courses = Course.objects.all()
    context_dict['courses'] = courses

    return render(request, 'csapp/home.html', context=context_dict)

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

def load_courses(request):
    year_of_studies = request.GET.get('year_of_studies')
    courses = Course.objects.filter(year_in_university = year_of_studies).order_by('name')
    return render(request, 'csapp/courses_dropdown_list.html', {'courses': courses})
    
                             
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

#for the chosen course to be displayed   
def postgraduate_course(request, course_name_slug):
    context_dict = {}
    try:
        course = Course.objects.get(slug=course_name_slug)
        context_dict['course'] = course
        context_dict['description'] = course.description
        #student = UserProfile.objects.get(user=request.user)
        #context_dict['student'] = student
        reviews = CourseRating.objects.order_by('-overall_rating').filter(course=course)
        if len(reviews) > 0:
            context_dict['lecturer_rating'] = lecturer_rating
            context_dict['engagement'] = engagement
            context_dict['informative'] = informative
            context_dict['comment'] = comment
    except Course.DoesNotExist:
        raise Http404("Course does not exist") 
    return render(request, 'csapp/course.html', context=context_dict)
    
#for the chosen course to be displayed  
#@Stefanos: I removed the year parameter as it wasnt running but i will try and figure it
# out later   
def undergraduate_course(request, course_name_slug):
    context_dict = {}
    try:
        course = Course.objects.get(slug=course_name_slug)
        #check if course has right corresponding year in URL
        if False:
            raise Http404("Wrong year")
        else:
            #student = User.objects.get(username=request.user)
            #context_dict['student'] = student
            context_dict['course'] = course
            context_dict['description'] = course.description
            reviews = CourseRating.objects.order_by('-overall_rating').filter(course=course)
            #context_dict['year'] = year
            if len(reviews) > 0:
                context_dict['lecturer_rating'] = lecturer_rating
                context_dict['engagement'] = engagement
                context_dict['informative'] = informative
                context_dict['comment'] = comment  
    except Course.DoesNotExist:
        context_dict['errors'] = 'This course does not exist'
        raise Http404("Course does not exist") 
    return render(request, 'csapp/course.html', context=context_dict)
    
    
@login_required    
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect(reverse('csapp:profile'))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context_dict = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'csapp/profile.html', context_dict)
    

