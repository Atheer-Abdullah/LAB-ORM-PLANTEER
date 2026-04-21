from django.contrib import admin
from .models import Plant, Comment, Country

class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",) 

class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_edible")

    list_filter = ("category", "is_edible", "countries")
    search_fields = ("name", "about")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "plant", "created_at")
    list_filter = ("plant",)

admin.site.register(Country, CountryAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)