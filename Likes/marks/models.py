from django.db import models

class Product(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Owner(models.Model):
    owner_id = models.IntegerField(blank=True)
    product_id = models.IntegerField(unique=True, blank=True)

    def __str__(self):
        return f"Owner id: {str(self.owner_id)}, product id: {str(self.product_id)}"