from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from flora.models import Plant 
from .models import Publisher

def add_publisher_view(request: HttpRequest):
    if request.method == "POST":
        
        name = request.POST.get("name")
        description = request.POST.get("description")
        established_at = request.POST.get("established_at")
        logo = request.FILES.get("logo")

        print("--- Attempting to add a new publisher ---")
        print(f"Name: {name}")
        print(f"Date: {established_at}")

        if name and established_at:
            try:
                new_publisher = Publisher(
                    name=name,
                    description=description,
                    established_at=established_at,
                    logo=logo
                )
                new_publisher.save()
                print("Saved to database successfully!")
                return redirect("publishers:publishers_list_view")
            except Exception as e:
                print(f"Database save failed: {e}")
        else:
            print("Missing required fields: Name or Establishment Date is missing from POST request")

    return render(request, "publishers/add_publisher.html")

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