from rest_framework import serializers
from .models.inventory import Inventory
from .models.user import User
from .models.order import Order
from .models.order_menu import OrderMenu
from .models.menu_inventory import MenuInventory
from .models.menu import Menu

# class MenuSerializer(serializers.Serializer):
#     name = serializers.CharField(label="Enter Menu Item name")
#     price = serializers.FloatField(label="Enter Menu Item Price")
#     category = serializers.CharField(label="Enter Menu Item Category")
#     description = serializers.CharField(label="Enter Menu Item Discription")
#     season_start = serializers.DateTimeField(label="Enter Menu Item Start Timestamp")
#     season_end = serializers.DateTimeField(label="Enter Menu Item end Timestamp")

# only for basic crud api, will decide to use it later when I ask group - Diego
class MenuSerializer(serializers.ModelSerializer):
    """
    Serializes the Menu Model
    """
    class Meta:
        model = Menu
        fields = "__all__"

class InventorySerializer(serializers.ModelSerializer):
    """
    Serializes the Inventory Model
    """
    class Meta:
        model = Inventory
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the User Model
    """
    class Meta:
        model = User
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes the Order Model
    """
    status = serializers.IntegerField()
    class Meta:
        model = Order
        fields = "__all__"
    
class OrderMenuSerializer(serializers.ModelSerializer):
    """
    Serializes the OrderMenu Model
    """
    class Meta:
        model = OrderMenu
        fields = "__all__"

class MenuInventorySerializer(serializers.ModelSerializer):
    """
    Serializes the MenuInventory Model
    """
    class Meta:
        model = MenuInventory
        fields = "__all__"

class WeatherSerializer(serializers.Serializer):
    """
    Serializes the Weather program as follows:\n
    - temperature field is a Float Field, representing current temperature at a location\n
    - icon field returns the icon to choose to represent the current weather condition\n
    - condition field returns a description of the current weather\n
    - surge field gives the multiplier for surge pricing\n
    """
    temperature = serializers.FloatField()
    icon = serializers.CharField()
    condition = serializers.CharField()
    surge = serializers.DictField()

class InventoryCountSerializer(serializers.Serializer):
    """
    Serializes the Inventory Count program as follows:\n
    - name represents the name of the inventory item\n
    - count represents the count of the named inventory item\n
    """
    name = serializers.CharField()
    count = serializers.IntegerField()

class SalesReportSerializer(serializers.Serializer):
    """
    Creates serialization for the Sales Report as follows:\n
    - element1 (Character Field)
    - element2 (Integer Field)
    - element3 (Decimal Field)
    """
    element1 = serializers.CharField()
    element2 = serializers.IntegerField()
    element3 = serializers.DecimalField(max_digits=10, decimal_places=2)

class ExcessReportSerializer(serializers.Serializer):
    """
    Creates serialization for the Excess Report as follows:\n
    - element1 (Character Field)
    - element2 (Integer Field)
    - element3 (Integer Field)
    """
    element1 = serializers.CharField()
    element2 = serializers.IntegerField()
    element3 = serializers.IntegerField()

class RestockReportSerializer(serializers.Serializer):
    """
    Creates serialization for the Restock Report as follows:\n
    - element1 (Character Field)
    - element2 (Integer Field)
    - element3 (Integer Field)
    """
    element1 = serializers.CharField()
    element2 = serializers.IntegerField()
    element3 = serializers.IntegerField()

class SellsTogetherSerializer(serializers.Serializer):
    """
    Creates serialization for the Sells Together Report as follows:\n
    - element1 (Character Field)
    - element2 (Character Field)
    - element3 (Integer Field)
    """
    element1 = serializers.CharField()
    element2 = serializers.CharField()
    element3 = serializers.IntegerField()