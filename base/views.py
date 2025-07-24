from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

def home(request):
    context = {}
    return render(request, 'base/home.html', context)

def coming_soon(request):
    context = {}
    return render(request, 'base/coming-soon.html', context)