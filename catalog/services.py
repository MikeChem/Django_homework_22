from catalog.models import Product
from django.core.cache import cache

def get_products_by_category(category_id):
    """
    Возвращает queryset продуктов указанной категории
    """
    return Product.objects.filter(category_id=category_id).select_related('category')

def get_cached_all_products():
    """
    Возвращает список всех продуктов из кэша или БД.
    """
    cache_key = 'all_products_list'
    products = cache.get(cache_key)

    if not products:
        # Если нет в кэше — загружаем из БД
        products = list(Product.objects.all().select_related('category'))
        cache.set(cache_key, products, 60 * 15)  # 15 минут

    return products