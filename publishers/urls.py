from django.urls import path
from . import views

app_name = "publishers"

urlpatterns = [
    path("add/", views.add_publisher_view, name="add_publisher_view"),
    path("all/", views.publishers_list_view, name="publishers_list_view"),
    path("detail/<publisher_id>/", views.publisher_detail_view, name="publisher_detail_view"),
]