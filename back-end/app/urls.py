from django.urls import path
from . import views

"""
This programs gives the url patterns needed to make the Backend API work
"""
urlpatterns = [
    path("", views.home, name="home")
]