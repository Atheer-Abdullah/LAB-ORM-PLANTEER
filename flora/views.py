from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Plant, Comment, Country
from publishers.models import Publisher


def all_plants_view(request: HttpRequest):
    category = request.GET.get("category")
    country_id = request.GET.get("country")

    plants = Plant.objects.all()
    countries = Country.objects.all()

    if category:
        plants = plants.filter(category=category)

    if country_id and country_id != "all":
        plants = plants.filter(countries__id=country_id)

    return render(request, "flora/all_plants.html", {
        "plants": plants,
        "categories": Plant.CategoryChoices.choices,
        "selected_category": category,
        "selected_country": country_id,
        "countries": countries,
    })

def plants_by_country_view(request: HttpRequest, country_id: int):
    plants = Plant.objects.filter(countries__id=country_id)
    countries = Country.objects.all()

    return render(request, "flora/all_plants.html", {
        "plants": plants,
        "countries": countries,
        "selected_country": str(country_id),
        "categories": Plant.CategoryChoices.choices,
    })

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

        publisher_id = request.POST.get("publisher")
        if publisher_id:
            new_plant.publisher = Publisher.objects.get(id=publisher_id)

        new_plant.save()
        new_plant.countries.set(request.POST.getlist("countries"))

        return redirect("flora:all_plants_view")

    return render(request, "flora/add_plant.html", {
        "categories": Plant.CategoryChoices.choices,
        "countries": Country.objects.all(),
        "publishers": Publisher.objects.all(),
    })


def plant_detail_view(request: HttpRequest, plant_id: int):
    plant = Plant.objects.select_related('publisher').get(pk=plant_id)
    comments = Comment.objects.filter(plant=plant).order_by('-created_at')

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id).order_by('?')[:3]

    return render(request, 'flora/plant_detail.html', {
        'plant': plant,
        'comments': comments,
        'related_plants': related_plants
    })

def add_comment_view(request: HttpRequest, plant_id: int):
    if request.method == "POST":
        plant_object = Plant.objects.get(pk=plant_id)
        new_comment = Comment(
            plant=plant_object,
            name=request.POST["name"],
            content=request.POST["content"]
        )
        new_comment.save()

    return redirect("flora:plant_detail_view", plant_id=plant_id)

def update_plant_view(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(pk=plant_id)

    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.category = request.POST["category"]
        plant.is_edible = "is_edible" in request.POST
        plant.is_helpful = "is_helpful" in request.POST

        publisher_id = request.POST.get("publisher")
        if publisher_id:
            plant.publisher = Publisher.objects.get(id=publisher_id)

        if "image" in request.FILES:
            plant.image = request.FILES["image"]

        plant.save()
        plant.countries.set(request.POST.getlist("countries"))

        return redirect("flora:plant_detail_view", plant_id=plant.id)

    return render(request, "flora/update_plant.html", {
        "plant": plant,
        "categories": Plant.CategoryChoices.choices,
        "countries": Country.objects.all(),
        "publishers": Publisher.objects.all(),
    })


def delete_plant_view(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(pk=plant_id)
    plant.delete()
    return redirect("flora:all_plants_view")


def search_plants_view(request: HttpRequest):
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        search_text = request.GET["search"]
        plants = Plant.objects.filter(name__icontains=search_text)

        if "order_by" in request.GET:
            if request.GET["order_by"] == "name":
                plants = plants.order_by("name")
            elif request.GET["order_by"] == "created_at":
                plants = plants.order_by("-created_at")
    else:
        plants = []

    return render(request, "flora/search_results.html", {"plants": plants})