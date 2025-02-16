from django.urls import path
from catalog.apps import CatalogConfig
from . import views
from catalog.views import products_list, products_detail
from django.conf import settings
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path("home/", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("", views.products_list, name='products_list'),
    path("products/<int:pk>/", views.products_detail, name='products_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
