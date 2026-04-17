from django.db import models

class Plant(models.Model):
    class CategoryChoices(models.TextChoices):
        TREE = 'Tree', 'Tree'
        FRUIT = 'Fruit', 'Fruit'
        VEGETABLE = 'Vegetable', 'Vegetable'

    # الحقول الأساسية
    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/", default="images/plant_default.jpg")
    category = models.CharField(
        max_length=20, 
        choices=CategoryChoices.choices, 
        default=CategoryChoices.TREE
    )
    
    # حقول التحقق (Boolean Fields)
    is_edible = models.BooleanField(default=False) # هل هي قابلة للأكل؟
    is_helpful = models.BooleanField(default=True) # هل هي مفيدة؟
    
    created_at = models.DateTimeField(auto_now_add=True)

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