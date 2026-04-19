from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from flora.models import Plant 

# Create your views here.

def home_view(request: HttpRequest):
   
    plants = Plant.objects.all().order_by('-id')[:3]
    return render(request, "main/index.html", {"plants": plants})

def contact_us_view(request: HttpRequest):
    return render(request, 'main/contact_us.html')

def contact_messages_view(request: HttpRequest):
    return render(request, "main/messages.html")

def mode_view(request: HttpRequest, mode):
    
    response = redirect(request.GET.get("next", "/"))

    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")

    return response