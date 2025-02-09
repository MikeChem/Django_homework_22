from django.contrib import admin

from .models import Category, Product

# Register your models here.
#admin.site.register(Student)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_category')
    search_fields = ('name_category', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_product', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name_product', 'description')