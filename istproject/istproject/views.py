from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Hey this is home page of django application")
    return render (request, "website/index.html")
def about(request):
    return HttpResponse("Hey this is about page of django application")

def contact(request):
    return HttpResponse("Hey this is contact page of django application")