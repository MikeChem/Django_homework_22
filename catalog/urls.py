from django.urls import path
from catalog.apps import CatalogConfig
from . import views
from catalog.views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ContactsView,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = "catalog"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", ProductListView.as_view(), name="products_list"),
    path("catalog/<int:pk>/", ProductDetailView.as_view(), name="products_detail"),
    path("catalog/create/", ProductCreateView.as_view(), name="products_create"),
    path(
        "catalog/<int:pk>/update/", ProductUpdateView.as_view(), name="products_update"
    ),
    path(
        "catalog/<int:pk>/delete/", ProductDeleteView.as_view(), name="products_delete"
    ),
    path("catalog/contacts/", ContactsView.as_view(), name="contacts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
