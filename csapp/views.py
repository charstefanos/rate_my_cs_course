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
    
    #Find the most viewed courses
    courses_viewed = Course.objects.order_by('-views')[:5]
    
    #Find the top rated courses
    all_courses = Course.objects.all()
    rated_courses={}
    for course in all_courses:
        reviews = CourseRating.objects.filter(course = course)
        number_reviews = 0
        sumOverallRating = 0 
        for review in reviews:
            overallRating = review.overall_rating
            sumOverallRating =  sumOverallRating + overallRating
            number_reviews = number_reviews + 1
        if number_reviews == 0:
            averageOverallRating = 0
        else:
            averageOverallRating = sumOverallRating / number_reviews
        rated_courses[course.name]=averageOverallRating
    
    #Sort the rated courses by the avg overall rating (i.e. the value)
    rated_courses = {k: v for k, v in sorted(rated_courses.items(), key=lambda item: item[1], reverse=True)}
    top_5 = list(rated_courses.keys())[:5]
    courses_rated=[]
    for k in top_5:
        courses_rated.append(Course.objects.get(name=k))
    context_dict['courses_viewed'] = courses_viewed
    context_dict['courses_rated'] = courses_rated

    return render(request, 'csapp/home.html', context=context_dict)

def undergraduate(request):
    coursesDict = {}
    courses = Course.objects.all()

    # Finds all the undergraduate courses
    # along with their information
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

    # Finds all the postgraduate courses
    # along with their information
    for course in courses:
        if course.year_in_university == 5:
            name = course.name
            year = course.year_in_university
            courseSlug = course.slug
            
            courseList = [year,courseSlug]
            coursesDict[name] = courseList

    return render(request, 'csapp/postgraduate.html', {'courses': coursesDict})

def course(request, course_name_slug):
    context_dict = {}
    try:
        # Anonymous users/Non users have no courses
        if request.user.is_anonymous:
            coursesTakenByUserList = None
        else:
            # Find the courses of the user
            coursesTakenByUserList = []
            user = request.user
            coursesTakenByUser = user.userprofile.courses.all()
        
            for course in coursesTakenByUser:
                coursesTakenByUserList.append(course.name)

        # Find details of the course
        # and increment its views
        course = Course.objects.get(slug=course_name_slug)
        course.views = course.views + 1
        course.save(update_fields=["views"]) 
    
        name = course.name
        description = course.description
        year = course.year_in_university
        slug = course.slug

        # Find all reviews for this course
        # and compute the various ratings
        reviews = CourseRating.objects.filter(course = course).order_by('-dateTime')
        reviewsDict = {}

        index = 0

        sumOverallRating = 0 
        sumLecturerRating = 0 
        sumEngagementRating = 0 
        sumInformativeRating = 0
        
        for review in reviews:
            reviewDict = {}

            student = review.student
            
            overallRating = review.overall_rating
            sumOverallRating =  sumOverallRating + overallRating
            
            lecturerRating = review.lecturer_rating
            sumLecturerRating = sumLecturerRating + lecturerRating

            engagementRating = review.engagement
            sumEngagementRating = sumEngagementRating + engagementRating
            
            informativeRating = review.informative
            sumInformativeRating = sumInformativeRating + informativeRating

            comment = review.comment

            reviewDict["student"] = student
            reviewDict["overallRating"] = 20*overallRating
            reviewDict["lecturerRating"] = 20*lecturerRating
            reviewDict["engagementRating"] = 20*engagementRating
            reviewDict["informativeRating"] = 20*informativeRating
            reviewDict["comment"] = comment

            reviewsDict[index] = reviewDict
            index = index + 1

        # Avoid division by 0 error
        if index == 0:
            averageOverallRating = 0
            averageLecturerRating = 0
            averageEngagementRating = 0
            averageInformativeRating = 0
        else:
        #Multiply by 20 (100*rating/5 = 20*rating) to get the rating in percentage 
            averageOverallRating = round(20*(sumOverallRating / index),1)
            averageLecturerRating = round(20*(sumLecturerRating / index),1)
            averageEngagementRating = round(20*(sumEngagementRating / index),1)
            averageInformativeRating = round(20*(sumInformativeRating / index),1)

        # Find all the users who have also this course
        # and have chosen to be contacted
        contactDict = {}
        users = UserProfile.objects.all()
        
        if request.user.is_anonymous == False:
            for user in users:
                if (user.current_student) and (user != request.user.userprofile) and (user.contact):
                    coursesTakenByUser = user.courses.all()

                    coursesTakenByContactUserList = []
                    for course in coursesTakenByUser:
                        coursesTakenByContactUserList.append(course.name)

                    # Allow only up to 5 students to be showcased
                    # in the need help box
                    index = 0
                    if (name in coursesTakenByContactUserList) and (index < 5):
                        contactDict[user] = user.email
                        index = index + 1

        # Dictionary that will be passed to the template
        context_dict["name"] = name
        context_dict["description"] = description
        context_dict["year"] = year
        context_dict["slug"] = slug
        context_dict["coursesTakenByUser"] = coursesTakenByUserList
        context_dict["contactUsers"] = contactDict
        context_dict["averageOverallRating"] = averageOverallRating
        context_dict["averageLecturerRating"] = averageLecturerRating
        context_dict["averageEngagementRating"] = averageEngagementRating
        context_dict["averageInformativeRating"] = averageInformativeRating
        context_dict["reviews"] = reviewsDict

    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    
    return render(request, 'csapp/course.html', {'courseInfo': context_dict})


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
    # When the year of studies changes in the register page
    # the jQuery code is triggered, csapp-filterCourses,
    # which then calls this view
    # This view then gets the year of studies
    # filters the courses based on that year of study
    # and passes the courses to a template
    # If successful, the jQuery will take those courses passed to the template
    # and add them to the courses drop-down list
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
            messages.error(request, 'Incorrect username or password')
            return redirect(reverse('csapp:login'))
    else:
        return render(request, 'csapp/login.html')

def search(request):
    # Creates a list of dictionaries
    # Each dictionary includes the name of a course, label
    # and its url, value

    # The list is then returned as a Json Response to a template,
    # which is then used by the jQuery code, csapp-searchBarAutocomplete,
    # to populate the search bar and link each course to its proper page
    # when its name is clicked
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

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('csapp:home'))
     
@login_required    
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
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
        messages.success(request, 'Profile deleted successfully!')
        return redirect(reverse('csapp:login'))
    else:
        user_delete_form = UserDeleteForm(instance=request.user)

    context_dict = {
        'user_delete_form': user_delete_form
    }

    return render(request, 'csapp/profile.html', context_dict)
 
@login_required
def write_review(request, course_name_slug):
    context_dict = {}
    ReviewPosted = False
    context_dict["reviewPosted"] = ReviewPosted
    
    course = Course.objects.get(slug=course_name_slug)
    context_dict["courseName"] = course.name
    
    user = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':

        try:
            review = CourseRating.objects.get(course = course, student = request.user.userprofile)
            review.delete()
        except CourseRating.DoesNotExist:
            pass
        
        review_form = ReviewForm(data=request.POST)
        
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.course = course
            review.student = user
            review.save()

            ReviewPosted = True
            context_dict["reviewPosted"] = ReviewPosted
        else:
            print(review_form.errors)
    else:
        review_form = ReviewForm()
        
    context_dict["reviewForm"] = review_form   
    return render(request, 'csapp/write_review.html', {'reviewInfo':context_dict})

@login_required
def my_reviews(request):
    student = UserProfile.objects.get(user=request.user)
    reviews_list = CourseRating.objects.filter(student=student)
    for review in reviews_list:
        review.overall_rating=20*review.overall_rating
        review.lecturer_rating=20*review.lecturer_rating
        review.engagement=20*review.engagement
        review.informative=20*review.informative

    return render(request, 'csapp/my_reviews.html', {'reviews_list': reviews_list})

@login_required
def delete_review(request, course_name_slug):

    if request.method == 'POST':
        course = Course.objects.get(slug=course_name_slug)
        review = CourseRating.objects.get(course = course, student = request.user.userprofile)
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect(reverse('csapp:my_reviews'))
    else:
        review_delete_form = ReviewDeleteForm()

    context_dict = {
        'review_delete_form': review_delete_form
    }

    return render(request, 'csapp/my_reviews.html', context_dict)
    

