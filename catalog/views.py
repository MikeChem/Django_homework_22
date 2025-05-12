# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from catalog.models import Product
from catalog.forms import ProductForm
from users.models import User  # ← если используешь в шаблонах

from django.views.decorators.cache import cache_page, never_cache
from django.http import JsonResponse
from django.core.cache import cache
from catalog.models import Product
from django.shortcuts import render, get_object_or_404
from catalog.models import Category
from catalog.services import get_products_by_category, get_cached_all_products

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return get_cached_all_products()

@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_object(self, queryset=None):
        """Получает объект из кэша или из БД"""
        obj = super().get_object(queryset)

        # Ручное кэширование данных продукта (можно использовать вместо cache_page)
        cache_key = f'product_{obj.id}'
        cached_product = cache.get(cache_key)

        if not cached_product:
            # Логика получения/обновления просмотров остаётся та же
            obj.views_counter += 1
            obj.save(update_fields=['views_counter'])
            # Сохраняем в кэше
            cache.set(cache_key, obj, 60 * 15)  # 15 минут

        return obj


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """Автоматически привязывает текущего пользователя как владельца"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete('all_products_list')  # Очистка кэша
        return response

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        """Проверяет, что пользователь — владелец или модератор"""
        obj = super().get_object(queryset)

        if obj.owner != self.request.user and not self.request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("У вас нет прав редактировать этот продукт.")
        return obj


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy("catalog:product_list")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.delete('all_products_list')  # Очистка кэша после удаления
        return response

    def get_object(self, queryset=None):
        """Проверяет, что пользователь — владелец или модератор"""
        obj = super().get_object(queryset)

        if obj.owner != self.request.user and not self.request.user.has_perm("catalog.delete_product"):
            raise PermissionDenied("У вас нет прав удалить этот продукт.")
        return obj


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")


def home(request):
    return render(request, "home.html")

def check_cache(request):
    cache_key = 'products_list'
    products = cache.get(cache_key)

    if products is None:
        # Кэш пропущен — делаем запрос к БД
        products = list(Product.objects.values('name_product', 'price', 'category__name_category'))
        cache.set(cache_key, products, 60 * 15)  # сохраняем на 15 минут
        return JsonResponse({
            "status": "miss",
            "message": "Данные взяты из БД и записаны в кэш",
            "count": len(products),
            "data": products
        }, safe=False)
    else:
        # Данные из кэша
        return JsonResponse({
            "status": "hit",
            "message": "Данные взяты из кэша",
            "count": len(products),
            "data": products
        }, safe=False)

def product_cache_status(request, pk):
    """Проверяет, находится ли продукт в кэше"""
    cache_key = f'product_{pk}'

    # Проверяем кэш
    cached_product = cache.get(cache_key)

    if cached_product is not None:
        return JsonResponse({
            'status': 'hit',
            'message': 'Продукт взят из кэша',
            'data': cached_product,
        })

    # Если нет в кэше — ищем в БД
    try:
        product = Product.objects.get(pk=pk)
        product_data = {
            'id': product.id,
            'name': product.name_product,
            'description': product.description,
            'price': product.price,
            'category': product.category.name_category if product.category else None,
            'views_counter': product.views_counter,
        }

        # Сохраняем в кэш
        cache.set(cache_key, product_data, 60 * 15)  # 15 минут

        return JsonResponse({
            'status': 'miss',
            'message': 'Продукт взят из БД',
            'data': product_data,
        })

    except Product.DoesNotExist:
        return JsonResponse({
            'error': 'Продукт не найден'
        }, status=404)

def products_by_category(request, category_id):
    # Получаем категорию из БД
    category = get_object_or_404(Category, id=category_id)

    # Используем сервисную функцию
    products = get_products_by_category(category_id)

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'catalog/products_by_category.html', context)

from catalog.services import get_cached_products_by_category

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = get_cached_products_by_category(category_id)

    return render(request, 'catalog/products_by_category.html', {
        'category': category,
        'products': products
    })
# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         message = request.POST.get("message")
#         return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
#     return render(request, "contacts.html")
