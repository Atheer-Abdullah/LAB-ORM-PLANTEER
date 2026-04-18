from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Plant

def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all()
    return render(request, "flora/all_plants.html", {"plants": plants})

def add_plant_view(request: HttpRequest):
    if request.method == "POST":
        new_plant = Plant(
            name=request.POST.get("name"),
            about=request.POST.get("about"),
            used_for=request.POST.get("used_for"),
            category=request.POST.get("category"),
            is_edible="is_edible" in request.POST,
            is_helpful="is_helpful" in request.POST,
        )

        if request.FILES.get("image"):
            new_plant.image = request.FILES.get("image")

        new_plant.save()
        return redirect("flora:all_plants_view")

    return render(request, "flora/add_plant.html", {
        "categories": Plant.CategoryChoices.choices
    })

def plant_detail_view(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    
    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id).order_by('?')[:3]
    
    return render(request, 'flora/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants
    })

def update_plant_view(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    
    if request.method == "POST":
        plant.name = request.POST.get("name")
        plant.about = request.POST.get("about")
        plant.used_for = request.POST.get("used_for")
        plant.category = request.POST.get("category")
        plant.is_edible = "is_edible" in request.POST
        plant.is_helpful = "is_helpful" in request.POST
        
        if request.FILES.get("image"):
            plant.image = request.FILES.get("image")
            
        plant.save()
        return redirect("flora:plant_detail_view", plant_id=plant.id)

    return render(request, "flora/update_plant.html", {
        "plant": plant,
        "categories": Plant.CategoryChoices.choices
    })

def delete_plant_view(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect("flora:all_plants_view")