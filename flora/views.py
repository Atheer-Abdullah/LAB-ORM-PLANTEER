from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Plant


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

        return redirect("flora:add_plant_view")

    return render(request, "flora/add_plant.html", {
        "categories": Plant.CategoryChoices.choices
    })


def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all()
    return render(request, "flora/all_plants.html", {"plants": plants})