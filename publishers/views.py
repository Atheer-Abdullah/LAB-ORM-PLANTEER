from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from flora.models import Plant 
from .models import Publisher
from .forms import PublisherForm  
from django.contrib import messages

# Create your views here.

def add_publisher_view(request: HttpRequest):
    if not request.user.is_superuser:
        messages.warning(request, "only admin can add publisher", "alert-warning")
        return redirect("main:home_view")

    publisher_form = PublisherForm()
    if request.method == "POST":
        publisher_form = PublisherForm(request.POST, request.FILES)
        if publisher_form.is_valid():
            publisher_form.save()
            messages.success(request, "Publisher added successfully!", "alert-success")
            return redirect("publishers:publishers_list_view")
    
    return render(request, "publishers/add_publisher.html", {"form": publisher_form})

def publishers_list_view(request: HttpRequest):
    publishers = Publisher.objects.all().order_by('-id')
    return render(request, "publishers/publishers.html", {"publishers": publishers})

def publisher_detail_view(request: HttpRequest, publisher_id: int):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    plants = Plant.objects.filter(publisher=publisher)
    return render(request, "publishers/publisher_page.html", {
        "publisher": publisher, 
        "plants": plants
    })

def update_publisher_view(request: HttpRequest, publisher_id: int):
    if not request.user.is_superuser:
        messages.warning(request, "only admin can update publisher", "alert-warning")
        return redirect("publishers:publishers_list_view")

    publisher = get_object_or_404(Publisher, id=publisher_id)
    if request.method == "POST":
        publisher_form = PublisherForm(instance=publisher, data=request.POST, files=request.FILES)
        if publisher_form.is_valid():
            publisher_form.save()
            messages.success(request, "Publisher updated successfully!", "alert-success")
            return redirect("publishers:publisher_detail_view", publisher_id=publisher.id)
    else:
        publisher_form = PublisherForm(instance=publisher)
    
    return render(request, "publishers/update_publisher.html", {
        "publisher": publisher,
        "form": publisher_form
    })

def delete_publisher_view(request: HttpRequest, publisher_id: int):
    if not request.user.is_superuser:
        messages.warning(request, "only admin can delete publisher", "alert-warning")
        return redirect("publishers:publishers_list_view")

    try:
        publisher = Publisher.objects.get(id=publisher_id)
        publisher.delete()
        messages.success(request, "Publisher deleted successfully!", "alert-success")
    except Exception as e:
        messages.error(request, "Couldn't Delete publisher", "alert-danger")
        
    return redirect("publishers:publishers_list_view")