from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from csapp.forms import *
from csapp.models import *
from django.http import Http404
from django.http import JsonResponse

def home(request):
    context_dict = {}
    course_list = Course.objects.order_by('-views')[:5]
    context_dict['courses'] = course_list

    return render(request, 'csapp/home.html', context=context_dict)

def undergraduate(request):
    coursesDict = {}
    courses = Course.objects.all()

    for course in courses:
        if course.year_in_university <= 4:
            name = course.name
            year = course.year_in_university
            courseSlug = course.slug
            
            courseList = [year,courseSlug]
            coursesDict[name] = courseList
        
    return render(request, 'csapp/undergraduate.html', {'courses': coursesDict})

def postgraduate(request):
    coursesDict = {}
    courses = Course.objects.all()

    for course in courses:
        if course.year_in_university == 5:
            name = course.name
            year = course.year_in_university
            courseSlug = course.slug
            
            courseList = [year,courseSlug]
            coursesDict[name] = courseList

    return render(request, 'csapp/postgraduate.html', {'courses': coursesDict})

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
    courses = Course.objects.filter(year_in_university__lte = year_of_studies).order_by('-year_in_university')
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
                messages.error(request, 'Your account is disabled')
                return redirect(reverse('csapp:login'))
            
        else:
            messages.error(request, 'Invalid login details supplied. Please try again.')
            return redirect(reverse('csapp:login'))
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
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile was updated successfully!')
            return redirect(reverse('csapp:profile'))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'csapp/profile.html', context_dict)

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, f'Your profile has been deleted successfully!')
        return redirect(reverse('csapp:login'))
    else:
        user_delete_form = UserDeleteForm(instance=request.user)

    context_dict = {
        'user_delete_form': user_delete_form
    }

    return render(request, 'csapp/profile.html', context_dict)

def search(request):
    courses = Course.objects.all()

    coursesList = []
    for course in courses:
        courseDictionary = {}
        name = course.name
        year = course.year_in_university
        if year <= 4:
            courseType = "undergraduate"
        else:
            courseType = "postgraduate"
        courseSlug = course.slug
        
        url = courseType + "/" + courseSlug
        
        courseDictionary["label"] = name
        courseDictionary["value"] = url
        coursesList.append(courseDictionary)

    return JsonResponse(coursesList, safe=False)
    
    
    

    

