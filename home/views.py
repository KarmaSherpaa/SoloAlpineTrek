from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, "index.html")

# def about(request):
#     return HttpResponse("This is about page")

# def contact(request):
#     return HttpResponse("This is contact page")

# def blog(request):
#     return HttpResponse("This is Blog page")

# def gallery(request):
#     return HttpResponse("This is Gallery page")

# def services(request):
#     return HttpResponse("This is Services page")

def destination(request):
    return render(request, "destination.html")

