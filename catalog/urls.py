from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig

urlpatterns = [
    path("home/", views.home, name="home"),
    path("catalog/", views.contacts, name="contacts"),
]
