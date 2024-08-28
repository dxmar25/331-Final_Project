from django.db import models

class Inventory(models.Model):
    """
    This is a Django Model of the Inventory Table

    It contains:\n
    - name: Name of inventory item\n
    - price: Price in dollars of the inventory item\n
    - stock: Current Stock of the Item\n
    - reorder_level: Level needed to reorder inventory item\n
    """
    name = models.TextField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=50)

    def clean(self):
        if self.price < 0 or self.stock < 0 or self.reorder_level < 0:
            raise ValueError("Price must be non-negative.")