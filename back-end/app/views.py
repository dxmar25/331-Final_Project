from django.shortcuts import  HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import connection
from .models.menu import *
from .models.user import *
from .models.inventory import *
from .models.menu_inventory import *
from .models.order import *
from .serializers import *
from rest_framework import viewsets, status, filters
from .weather import getAggregateData
from django.db import transaction

# Create your views here.
def home(request):
    return HttpResponse("Hello world")

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset
 
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        inventory_id = instance.id

        with transaction.atomic():
            MenuInventory.objects.filter(inventory_id=inventory_id).delete()
            self.perform_destroy(instance)
        #w
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        existing_user = User.objects.filter(email=email).first()

        ## ignore duplicate user, update user with same email
        if existing_user:
            # Update the existing user with the new data
            serializer = self.get_serializer(existing_user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Create a new user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ('=id', '=status')
    ordering_fields = '__all__'

    #USING THE DEFAULT UPPDATE.

    # def update(self, request, pk=None):
    #     instance = self.get_object()
    #     serializer = OrderSerializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')  # Assuming you're passing order_id as a query parameter
        id = self.request.query_params.get('id')
        
        if id:
            queryset = queryset.filter(id=id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     edit_id = self.request.query_params.get('edit_id')
    #     print(edit_id)
    #     existing_order = User.objects.filter(id=edit_id).first()
    #     ## update order with same id
    #     if existing_order:
    #         # Update the existing order with the new data
    #         serializer = self.get_serializer(existing_order, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class OrderMenuViewSet(viewsets.ModelViewSet):
    queryset = OrderMenu.objects.all()
    serializer_class = OrderMenuSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('=id', '=order__id')
    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')  
        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(id=id)
        if order_id:
            queryset = queryset.filter(order__id=order_id)
        return queryset
    def delete(self, request):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id') 
        queryset_to_delete = queryset.filter(order__id=order_id)
        queryset_to_delete.delete()

        return Response({"message": "Queryset deleted successfully"})
    
class MenuInventoryViewSet(viewsets.ModelViewSet):
    queryset = MenuInventory.objects.all()
    serializer_class = MenuInventorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields =('=id', '=menu_id')
    def get_queryset(self):
        queryset = super().get_queryset()
        menu_id = self.request.query_params.get('menu_id')
        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(id=id)
        if menu_id:
            queryset = queryset.filter(menu_id=menu_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def check_inventory(self, request):
        print("calling check_inventory")
        # Get menu IDs and deductions from request data
        menu_ids = request.data.get('menu_ids', [])
        deductions = request.data.get('deductions', [])
        if not menu_ids:
            return Response({"error": "No menu IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        pending_orders = Order.objects.filter(status=0)
        order_ids = [order.id for order in pending_orders]
        pending_deductions = {}
        for id in order_ids:
            pending_order_menu = OrderMenu.objects.filter(order = id)
            for order_menu in pending_order_menu:
                pending_menu_id = order_menu.menu.id
                pending_deductions[pending_menu_id] = pending_deductions.get(pending_menu_id, 0) + order_menu.quantity; 
        for id, quantity in pending_deductions.items():
            deductions.append({"id": id, "quantity": quantity})
        insufficient_items = []

        # Create a dictionary to store current inventory stock for fast lookup
        inventory_stock = {inventory.id: inventory.stock for inventory in Inventory.objects.all()}
        # Apply deductions to inventory stock
        for deduction in deductions:
            # Find all MenuInventory entries for the menu ID
            menu_inventories = MenuInventory.objects.filter(menu=deduction['id'])
            for menu_inventory in menu_inventories:
                inventory = menu_inventory.inventory
                if inventory.id in inventory_stock:
                    inventory_stock[inventory.id] -= deduction['quantity']
        # print(inventory_stock)
        # Check inventory for each menu item
        for menu_id in menu_ids:
            # Find all MenuInventory entries for the menu ID
            menu_inventories = MenuInventory.objects.filter(menu=menu_id)
            for menu_inventory in menu_inventories:
                inventory = menu_inventory.inventory
                if inventory.id in inventory_stock:
                    if inventory_stock[inventory.id] <= 0:
                        insufficient_items.append({"id": menu_id, "insufficient_inventory_quantity": inventory_stock[inventory.id]})
        # print("Insufficient_items: " + str(insufficient_items))
        return Response({"insufficient_items": insufficient_items}, status=status.HTTP_200_OK)

class WeatherAPIView(APIView):
    def get(self, request):
        weather_data = getAggregateData()
        serializer = WeatherSerializer(weather_data)
        return Response(serializer.data)

class ProductUsageChart(APIView):
    def get(self, request):
        start_date = request.query_params.get('startDate', None)
        end_date = request.query_params.get('endDate', None)
        print(start_date)
        print(end_date)

        query = """ 
                SELECT i.name, COUNT(mi.inventory_id) AS repetition_count
                FROM app_menuinventory AS mi
                JOIN app_inventory AS i ON mi.inventory_id = i.id
                JOIN app_menu AS m ON mi.menu_id = m.id
                WHERE m.id IN (
                    SELECT om.menu_id
                    FROM app_ordermenu AS om
                    JOIN app_order AS o ON om.order_id = o.id
                    WHERE o.timestamp BETWEEN %s AND %s
                )
                GROUP BY i.name
                ORDER BY repetition_count DESC;
                """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [start_date, end_date]) # add start and end
            rows = cursor.fetchall()

        inventory_counts = [] 
        for row in rows:
            name, count = row
            inventory_counts.append({
                "name": name,
                "count": count
            })
        
        serializer = InventoryCountSerializer(data=inventory_counts, many=True) # this might not work
        serializer.is_valid()
        return Response(serializer.data)
    
class SalesReportChart(APIView):
    def get(self, request):
        start_date = request.query_params.get('startDate', None)
        end_date = request.query_params.get('endDate', None)
        print(start_date)
        print(end_date)

        query = """
                SELECT m.name, COUNT(om.quantity) AS element1, SUM(m.price * om.quantity) AS element2
                FROM app_ordermenu om
                JOIN app_order o ON om.order_id = o.id
                JOIN app_menu m ON om.menu_id = m.id
                WHERE o.timestamp BETWEEN %s AND %s
                GROUP BY m.name
                ORDER BY element1 DESC;                        
                """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [start_date, end_date]) # add start and end
            rows = cursor.fetchall()

        response = []
        for row in rows:
            element1, element2, element3 = row
            response.append({
                "element1": element1, # name
                "element2": element2, # Quanity sold
                "element3": element3  # Revenue from item
            })

        serializer = SalesReportSerializer(data=response, many=True) # this might not work
        serializer.is_valid()
        return Response(serializer.data)
    
class ExcessReportView(APIView):
    def get(self, request):
        timestamp = request.query_params.get('startDate', None)

        query = """
            SELECT i.name, subquery.amount_used, i.stock AS current_stock
            FROM app_inventory AS i
            LEFT JOIN (
                SELECT mi.inventory_id, COUNT(*) AS amount_used
                FROM app_menuinventory AS mi
                JOIN app_menu AS m ON mi.menu_id = m.id
                JOIN app_ordermenu AS om ON m.id = om.menu_id
                JOIN app_order AS o ON om.order_id = o.id
                WHERE o.timestamp BETWEEN '2022-03-29 00:00:00' AND NOW()
                GROUP BY mi.inventory_id
            ) AS subquery ON i.id = subquery.inventory_id
            WHERE subquery.amount_used < (i.stock * 0.1)
            ORDER BY subquery.amount_used;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [timestamp])
            rows = cursor.fetchall()

        response = []
        for row in rows:
            element1, element2, element3 = row
            response.append({
                "element1": element1, #Item name
                "element2": element2, #Quantity used
                "element3": element3, #Current stock
            })

        serializer = ExcessReportSerializer(data=response, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    

class RestockReportView(APIView):
    def get(self, request):
        query = """
            SELECT name, stock AS current_stock, reorder_level
            FROM app_inventory
            WHERE stock < reorder_level
            ORDER BY current_stock;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        response = []
        for row in rows:
            element1, element2, element3 = row
            response.append({
                "element1": element1, #item name
                "element2": element2, #current amount
                "element3": element3, #Restock Level
            })

        serializer = RestockReportSerializer(data=response, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    
class SellsTogetherView(APIView):
    def get(self, request):
        start_date = request.query_params.get('startDate', None)
        end_date = request.query_params.get('endDate', None)

        query = """
            SELECT m1.name AS item1, m2.name AS item2, COUNT(*) AS count
            FROM app_ordermenu om1
            JOIN app_ordermenu om2 ON om1.order_id = om2.order_id AND om1.menu_id < om2.menu_id
            JOIN app_menu m1 ON om1.menu_id = m1.id
            JOIN app_menu m2 ON om2.menu_id = m2.id
            JOIN app_order o ON om1.order_id = o.id
            WHERE o.timestamp BETWEEN %s AND %s
            GROUP BY m1.name, m2.name
            ORDER BY count DESC
            LIMIT 10;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [start_date, end_date])
            rows = cursor.fetchall()

        response = []
        for row in rows:
            element1, element2, element3 = row
            response.append({
                "element1": element1,
                "element2": element2,
                "element3": element3,
            })

        serializer = SellsTogetherSerializer(data=response, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)