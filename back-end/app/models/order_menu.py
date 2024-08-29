from django.db import models
from .order import Order
from .menu import Menu
#Junction table: order_menu

# represents the Junction table
class OrderMenu(models.Model):
    """
    This is a Django Model of the Order Menu Table

    It contains:\n
    - order: Foregin key for order table\n
    - menu: Foregin key for menu table\n
    - quantity: Integer Field for quantity of Order\n
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)

