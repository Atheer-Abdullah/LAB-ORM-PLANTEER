from django.db import models

# Create your models here.

class Publisher(models.Model):

    name = models.CharField(max_length=1024)
    
    description = models.TextField()
    
    logo = models.ImageField(upload_to="images/", default="images/default.jpg")
    
    established_at = models.DateField() 
    
    website = models.URLField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.name}"