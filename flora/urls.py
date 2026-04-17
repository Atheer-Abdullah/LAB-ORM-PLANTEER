from django.urls import path
from . import views

app_name = "flora"

urlpatterns = [
    path("new/", views.add_plant_view, name="add_plant_view"),
    path("all/", views.all_plants_view, name="all_plants_view"),
    path("detail/<plant_id>/", views.plant_detail_view, name="plant_detail_view"),
]