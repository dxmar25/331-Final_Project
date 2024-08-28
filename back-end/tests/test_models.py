# tests/test_models.py
import pytest
from django.test import TestCase
from app.models.inventory import Inventory
from app.models.menu import Menu
from app.models.order import Order
from app.models.inventory import Inventory
from app.models.menu_inventory import MenuInventory
from app.models.order_menu import OrderMenu
from django.utils import timezone
from app.serializers import *
from app import views 
from app.urls import urlpatterns 
from rest_framework import status
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APIRequestFactory
from app.views import WeatherAPIView, SellsTogetherView
from django.db import connection
from datetime import datetime, timedelta
from unittest.mock import patch
from rest_framework.test import APITestCase
from app.weather import getCurrentInfo, getTemperature, getWeatherIcon, getWeatherConditionName, getAggregateData, weatherData 

@pytest.mark.django_db
class TestInventoryModel(TestCase):
    def test_inventory_creation(db):
        inventory = Inventory.objects.create(
            name='Test Product',
            price=9.99,
            stock=100,
            reorder_level=10
        )
        assert inventory.name == 'Test Product'
        assert inventory.price == 9.99
        assert inventory.stock == 100
        assert inventory.reorder_level == 10

    def test_inventory_str_representation(self):
        inventory = Inventory.objects.create(
            name='Test Product',
            price=9.99,
            stock=100,
            reorder_level=10
        )
        assert str(inventory.name) == 'Test Product'

    def test_inventory_price_positive(self):
        with pytest.raises(ValueError):
            inventory = Inventory.objects.create(
                name='Test Product',
                price=-9.99,
                stock=100,
                reorder_level=10
            )
            inventory.full_clean()

    def test_inventory_stock_non_negative(self):
        with pytest.raises(ValueError):
            inventory = Inventory.objects.create(
                name='Test Product',
                price=9.99,
                stock=-100,
                reorder_level=10
            )
            inventory.full_clean()

    def test_inventory_reorder_level_non_negative(self):
        with pytest.raises(ValueError):
            inventory = Inventory.objects.create(
                name='Test Product',
                price=9.99,
                stock=100,
                reorder_level=-10
            )
            inventory.full_clean()

# Add more model tests here
class TestMenu(TestCase):
    def test_menu_creation(self):
        menu_item = Menu.objects.create(
            name='Cheeseburger',
            price=5.99,
            category=Menu.CategoryOptions.BURGERS,
            description='A classic burger with cheese',
            season_start=timezone.now(),
            season_end=timezone.now() + timezone.timedelta(days=30),
            display=True,
            image='https://example.com/cheeseburger.jpg'
        )
        assert menu_item.name == 'Cheeseburger'
        assert menu_item.price == 5.99
        assert menu_item.category == Menu.CategoryOptions.BURGERS
        assert menu_item.description == 'A classic burger with cheese'
        assert menu_item.season_start <= timezone.now()
        assert menu_item.season_end >= timezone.now()
        assert menu_item.display
        assert menu_item.image == 'https://example.com/cheeseburger.jpg'

    def test_menu_serializer_validation(self):
        """
        Test that the serializer validates data correctly
        """
        invalid_data = {
            'name': 'Cheeseburger',
            'price': -5.99,  # Invalid negative price
            'category': 99,  # Invalid category value
            'description': 'A classic burger with cheese',
            'season_start': timezone.now().isoformat(),
            'season_end': (timezone.now() - timezone.timedelta(days=30)).isoformat(),  # Invalid season_end before season_start
            'display': True,
            'image': 'https://example.com/cheeseburger.jpg'
        }
        serializer = MenuSerializer(data=invalid_data)
        assert not serializer.is_valid()

class TestURLs(TestCase):
    def test_home_url(self):    
        """
        Test that the home URL is resolved correctly
        """
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

@pytest.mark.django_db
class TestWeatherAPIView:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.view = WeatherAPIView.as_view()
        self.client = APIClient()

    def test_get_weather_data(self, mocker):
        """
        Test that the GET request returns weather data
        """
        # Mock the getAggregateData function
        mock_data = {
            'temperature': 78.76,
            'icon': '04d',
            'condition': 'Cloudy',
            'surge': {
                'Burgers': 1.1,
                'Baskets': 1.1,
                'ShakesnSweets': 1.1,
                'Sandwiches': 1.1,
                'Beverages': 1.1,
                'Sides': 1.1,
                'Sauces': 1.1
            }
        }
        mocker.patch("app.views.getAggregateData", return_value=mock_data)

        # Make a GET request to the view
        url = reverse("weather_api")
        request = self.factory.get(url)
        response = self.view(request)
        print(response)
        # Assert the response status code and data
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_data

    def test_get_weather_data_client(self, mocker):
        """
        Test the GET request using the API client
        """
        # Mock the getAggregateData function
        mock_data = {
            'temperature': 78.76,
            'icon': '04d',
            'condition': 'Cloudy',
            'surge': {
                'Burgers': 1.1,
                'Baskets': 1.1,
                'ShakesnSweets': 1.1,
                'Sandwiches': 1.1,
                'Beverages': 1.1,
                'Sides': 1.1,
                'Sauces': 1.1
            }
        }
        mocker.patch("app.views.getAggregateData", return_value=mock_data)

        # Make a GET request using the API client
        url = reverse("weather_api")
        response = self.client.get(url)

        # Assert the response status code and data
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_data

class TestWeather:
    def test_get_aggregate_data(monkeypatch):
        
        getCurrentInfo()
        expected_data = {
        "temperature": getTemperature(),
        "icon": getWeatherIcon(),
        "condition": getWeatherConditionName(),
        "surge": {"Burgers": 1.1, "Baskets": 1.1, "ShakesnSweets": 1.1, "Sandwiches": 1.1, "Beverages": 1.1, "Sides": 1.1, "Sauces": 1.1}
        }

        assert getAggregateData() == expected_data

@pytest.fixture
def sample_weather_data():
    return {
        'weather': [
            {'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}
        ]
    }

def test_get_weather_condition_name_unknown(sample_weather_data):
    sample_weather_data["weather"][0]["id"] = 999  # Unknown condition
    with patch('app.weather.weatherData', sample_weather_data):
        assert getWeatherConditionName() == "Unknown"

def test_get_weather_condition_name_Clear(sample_weather_data):
    sample_weather_data["weather"][0]["id"] = "800"  # Unknown condition
    with patch('app.weather.weatherData', sample_weather_data):
        assert getWeatherConditionName() == "Clear"

def test_get_weather_condition_name_Thunder(sample_weather_data):
    sample_weather_data["weather"][0]["id"] = 2  # Unknown condition
    with patch('app.weather.weatherData', sample_weather_data):
        assert getWeatherConditionName() == "Thunderstorm"

def test_get_weather_condition_name_Drizzy(sample_weather_data):
    sample_weather_data["weather"][0]["id"] = 3  # Unknown condition
    with patch('app.weather.weatherData', sample_weather_data):
        assert getWeatherConditionName() == "Drizzle"

def test_get_weather_condition_name_Rain(sample_weather_data):
    sample_weather_data["weather"][0]["id"] = 5  # Unknown condition
    with patch('app.weather.weatherData', sample_weather_data):
        assert getWeatherConditionName() == "Rain"

def test_get_weather_condition_name_Snow(sample_weather_data):
    sample_weather_data["weather"][0]["id"] = 6  # Unknown condition
    with patch('app.weather.weatherData', sample_weather_data):
        assert getWeatherConditionName() == "Snow"

def test_get_weather_condition_name_Obscure(sample_weather_data):
    sample_weather_data["weather"][0]["id"] = 7  # Unknown condition
    with patch('app.weather.weatherData', sample_weather_data):
        assert getWeatherConditionName() == "Obscure"


class MenuViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu_list_url = reverse('menu-list')
        self.menu_item_1 = Menu.objects.create(
            name='Item 1',
            category=Menu.CategoryOptions.BURGERS,
            price=9.99,
            season_start=datetime.now(),
            season_end=datetime.now() + timedelta(days=30)
        )
        self.menu_item_2 = Menu.objects.create(
            name='Item 2',
            category=Menu.CategoryOptions.SANDWICHES,
            price=7.99,
            season_start=datetime.now(),
            season_end=datetime.now() + timedelta(days=30)
        )

    def test_get_menu_list(self):
        response = self.client.get(self.menu_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_menu_list_with_category_filter(self):
        response = self.client.get(f"{self.menu_list_url}?category={Menu.CategoryOptions.BURGERS}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Item 1')

    def test_create_menu_item(self):
        data = {
            'name': 'New Item',
            'category': Menu.CategoryOptions.SHAKESNSWEETS,
            'price': 5.99,
            'season_start': datetime.now().isoformat(),
            'season_end': (datetime.now() + timedelta(days=30)).isoformat()
        }
        response = self.client.post(self.menu_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)
        self.assertEqual(Menu.objects.get(name='New Item').category, Menu.CategoryOptions.SHAKESNSWEETS)

class MenuInventoryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu_item_1 = Menu.objects.create(
            name='Item 1',
            category=Menu.CategoryOptions.BURGERS,
            price=9.99,
            season_start=datetime.now(),
            season_end=datetime.now() + timedelta(days=30)
        )
        self.inventory_item_1 = Inventory.objects.create(name='Ingredient 1', price=2.99, stock=100, reorder_level=20)
        self.menu_inventory_item_1 = MenuInventory.objects.create(menu=self.menu_item_1, inventory=self.inventory_item_1)

    def test_get_menu_inventory_list(self):
        url = reverse('menu_inventory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_menu_inventory_item(self):
        url = reverse('menu_inventory-list')
        menu_item_2 = Menu.objects.create(
            name='Item 2',
            category=Menu.CategoryOptions.SANDWICHES,
            price=7.99,
            season_start=datetime.now(),
            season_end=datetime.now() + timedelta(days=30)
        )
        inventory_item_2 = Inventory.objects.create(name='Ingredient 2', price=1.99, stock=50, reorder_level=10)
        data = {
            'menu': menu_item_2.pk,
            'inventory': inventory_item_2.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuInventory.objects.count(), 2)

    def test_update_menu_inventory_item(self):
        url = reverse('menu_inventory-detail', kwargs={'pk': self.menu_inventory_item_1.pk})
        inventory_item_3 = Inventory.objects.create(name='Ingredient 3', price=3.99, stock=75, reorder_level=15)
        data = {
            'inventory': inventory_item_3.pk
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_inventory_item_1.refresh_from_db()
        self.assertEqual(self.menu_inventory_item_1.inventory, inventory_item_3)

    def test_delete_menu_inventory_item(self):
        url = reverse('menu_inventory-detail', kwargs={'pk': self.menu_inventory_item_1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MenuInventory.objects.count(), 0)


class RestockReportViewTestCase(APITestCase):
    @patch('app.views.connection.cursor')
    def test_get_restock_report(self, mock_cursor):
        # Mock the execute method of the cursor
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
            ('Item1', 10, 20),
            ('Item2', 15, 25)
        ]

        url = reverse('restock-report-chart-data-api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['element1'], 'Item1')
        self.assertEqual(response.data[0]['element2'], 10)
        self.assertEqual(response.data[0]['element3'], 20)
        self.assertEqual(response.data[1]['element1'], 'Item2')
        self.assertEqual(response.data[1]['element2'], 15)
        self.assertEqual(response.data[1]['element3'], 25)

class SalesReportChartTestCase(APITestCase):
    @patch('app.views.connection.cursor')
    def test_get_sales_report(self, mock_cursor):
        # Mock the execute method of the cursor
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
            ('Item1', 10, 200),
            ('Item2', 5, 100),
        ]

        url = reverse('sales-report-chart-data-api')
        response = self.client.get(url, {'startDate': '2023-01-01', 'endDate': '2023-01-31'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['element1'], 'Item1')
        self.assertEqual(response.data[0]['element2'], 10)
        self.assertEqual(response.data[0]['element3'], '200.00')
        self.assertEqual(response.data[1]['element1'], 'Item2')
        self.assertEqual(response.data[1]['element2'], 5)
        self.assertEqual(response.data[1]['element3'], '100.00')