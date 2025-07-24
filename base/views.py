from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

def home(request):
    context = {}
    return render(request, 'base/home.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)

def contact(request):
    context = {}
    return render(request, 'base/contact.html', context)

def legal(request):
    context = {}
    return render(request, 'base/legal.html', context)

def coming(request):
    context = {}
    return render(request, 'base/coming.html', context)