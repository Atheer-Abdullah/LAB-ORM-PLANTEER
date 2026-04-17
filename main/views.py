from django.shortcuts import render
from django.http import HttpRequest

from flora.models import Plant 

def home_view(request: HttpRequest):

    plants = Plant.objects.all().order_by('-id')[:3]
    return render(request, "main/index.html", {"plants": plants})

def contact_us_view(request: HttpRequest):
    return render(request, 'main/contact_us.html')

def contact_messages_view(request: HttpRequest):
    return render(request, "main/messages.html")