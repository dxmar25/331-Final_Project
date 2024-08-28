from django.db import models
from .menu import Menu
from .inventory import Inventory
#Junction table: menu_inventory
class MenuInventory(models.Model):
    """
    This is a Django Model of the Menu Inventory Table

    It contains:\n
    - menu: Foregin key for Menu table\n
    - inventory: Foregin key for Inventory table\n
    """
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING)
    
    # class Meta:
    #     unique_pair = ('menu', 'inventory')
