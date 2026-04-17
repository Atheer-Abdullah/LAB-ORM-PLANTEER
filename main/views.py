from django.shortcuts import render
from django.http import HttpRequest

def home_view(request: HttpRequest):
    
    return render(request, "main/index.html")

def contact_us_view(request: HttpRequest):

    return render(request, "main/contact.html")

def contact_messages_view(request: HttpRequest):
    
    return render(request, "main/messages.html")