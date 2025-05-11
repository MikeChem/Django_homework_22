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


@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_counter += 1
        obj.save()
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


# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         message = request.POST.get("message")
#         return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
#     return render(request, "contacts.html")
