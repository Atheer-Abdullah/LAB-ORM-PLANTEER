from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Plant, Comment, Country
from publishers.models import Publisher

def all_plants_view(request: HttpRequest, country_id=None):
    category = request.GET.get("category")
    c_id = country_id or request.GET.get("country")
    publisher_id = request.GET.get("publisher")
    region_name = request.GET.get("native_region")
    is_edible = request.GET.get("is_edible")
    is_helpful = request.GET.get("is_helpful")

    plants = Plant.objects.all().select_related('publisher')
    countries = Country.objects.all()
    publishers = Publisher.objects.all()

    if category:
        plants = plants.filter(category=category)

    if c_id and str(c_id) != "all":
        plants = plants.filter(countries__id=c_id)

    if publisher_id:
        plants = plants.filter(publisher_id=publisher_id)

    if region_name:
        plants = plants.filter(countries__name__icontains=region_name)

    if is_edible == "True":
        plants = plants.filter(is_edible=True)

    if is_helpful == "True":
        plants = plants.filter(is_helpful=True)

    return render(request, "flora/all_plants.html", {
        "plants": plants,
        "categories": Plant.CategoryChoices.choices,
        "selected_category": category,
        "selected_country": str(c_id) if c_id else None,
        "countries": countries,
        "publishers": publishers,
    })

def plant_detail_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant.objects.select_related('publisher'), pk=plant_id)
    comments = Comment.objects.filter(plant=plant).order_by('-created_at')
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id).order_by('?')[:3]
    return render(request, 'flora/plant_detail.html', {
        'plant': plant, 
        'comments': comments, 
        'related_plants': related_plants
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

def update_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
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
    plant = get_object_or_404(Plant, pk=plant_id)
    plant.delete()
    return redirect("flora:all_plants_view")

def add_comment_view(request: HttpRequest, plant_id: int):
    if request.method == "POST":
        plant_object = get_object_or_404(Plant, pk=plant_id)
        Comment.objects.create(
            plant=plant_object, 
            name=request.POST["name"], 
            content=request.POST["content"]
        )
    return redirect("flora:plant_detail_view", plant_id=plant_id)

def search_plants_view(request: HttpRequest):
    search_text = request.GET.get("search", "")
    plants = Plant.objects.filter(name__icontains=search_text) if len(search_text) >= 3 else []
    return render(request, "flora/search_results.html", {"plants": plants})