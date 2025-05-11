# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from catalog.forms import ProductForm
from catalog.models import Product
from django.urls import reverse_lazy, reverse


class ProductListView(ListView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_list.html' # added template name

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'  # added template name
    form_class = ProductForm

    def get_object(self, queryset=None):
        # Переопределение метода get_object для настройки логики выбора объекта
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")
    template_name = 'catalog/product_form.html' # added template name

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")
    template_name = 'catalog/product_form.html' # added template name


    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")
    template_name = 'catalog/product_confirm_delete.html' # added template name
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте любые дополнительные переменные в контекст, если необходимо
        return context

def home(request):
    return render(request, "home.html")


# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         message = request.POST.get("message")
#         return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
#     return render(request, "contacts.html")
