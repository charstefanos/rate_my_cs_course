from django.shortcuts import render

def home(request):
    return render(request, 'csapp/home.html')
