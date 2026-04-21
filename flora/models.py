from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to="images/flags/", default="images/flags/default_flag.png")

    def __str__(self):
        return self.name

class Plant(models.Model):
    class CategoryChoices(models.TextChoices):
        TREE = 'Tree', 'Tree'
        FRUIT = 'Fruit', 'Fruit'
        VEGETABLE = 'Vegetable', 'Vegetable'

    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/", default="images/plant_default.jpg")
    category = models.CharField(
        max_length=20, 
        choices=CategoryChoices.choices, 
        default=CategoryChoices.TREE
    )
    
    is_edible = models.BooleanField(default=False) 
    is_helpful = models.BooleanField(default=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)

    countries = models.ManyToManyField(Country, related_name="plants")

    def __str__(self):
        return self.name

    def get_status_message(self):
        if self.is_edible and self.is_helpful:
            return "This plant is both edible and very helpful!"
        elif self.is_edible and not self.is_helpful:
            return "This plant is edible but has no known major benefits."
        elif not self.is_edible and self.is_helpful:
            return "Not for eating, but very useful for other purposes."
        else:
            return "This plant is neither edible nor particularly helpful."


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.plant.name}"