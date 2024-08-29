"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app import views
from rest_framework import routers

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# if other MenuSerializer and MenuViewSet are commented out, need to make router for that as well
routerMenu = routers.DefaultRouter()
routerMenu.register('menu', views.MenuViewSet)

routerInventory = routers.DefaultRouter()
routerInventory.register('inventory', views.InventoryViewSet)

routerUser = routers.DefaultRouter()
routerUser.register('user', views.UserViewSet)

routerOrder = routers.DefaultRouter()
routerOrder.register('order', views.OrderViewSet)
# routerOrder.register("order/<int:pk>", views.OrderViewSet)
routerOrderMenu = routers.DefaultRouter()
routerOrderMenu.register('order_menu', views.OrderMenuViewSet)

routerMenuInventory = routers.DefaultRouter()
routerMenuInventory.register('menu_inventory', views.MenuInventoryViewSet, basename='menu_inventory')

urlpatterns = [
    path("", include("app.urls")),
    # path("admin/", admin.site.urls),
    # path("api/menu/", views.MenuApiView.as_view(), name = 'menu_api'),
    path("", include(routerMenu.urls)),
    path("", include(routerInventory.urls)),
    path("", include(routerUser.urls)),
    path("", include(routerOrder.urls)),
    path("", include(routerOrderMenu.urls)),
    path("", include(routerMenuInventory.urls)),
    path('weather/', views.WeatherAPIView.as_view(), name='weather_api'),
    path('product_usage_chart_data/', views.ProductUsageChart.as_view(), name='product-usage-chart-data-api'),
    path('sales_report/', views.SalesReportChart.as_view(), name='sales-report-chart-data-api'),
    path('excess_report/', views.ExcessReportView.as_view(), name='excess-report-chart-data-api/'),
    path('restock_report/', views.RestockReportView.as_view(), name='restock-report-chart-data-api'),
    path('sells_together/', views.SellsTogetherView.as_view(), name='sells-together-chart-data-api'),

    path('check_inventory/', views.MenuInventoryViewSet.as_view({'post': 'check_inventory'}), name="check_inventory")
]

urlpatterns += staticfiles_urlpatterns()