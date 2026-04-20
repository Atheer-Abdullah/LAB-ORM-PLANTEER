from django.contrib import admin
from .models import Plant,Comment

class PlantAdmin(admin.ModelAdmin):
   
    list_display = ("name", "category", "is_edible")
   
    list_filter = ("category", "is_edible")

class CommentAdmin(admin.ModelAdmin):

    list_display = ("name", "plant", "created_at")

    list_filter = ("plant",)

admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)