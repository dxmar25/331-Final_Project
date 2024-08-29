from django.contrib import admin
from .models import *


"""
This python script registers all the models into the Django Admin
"""

admin.site.register(Inventory)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(OrderMenu)
admin.site.register(MenuInventory)