from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from catalog.models import Product
from django.urls import reverse_lazy, reverse


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        # Переопределение метода get_object для настройки логики выбора объекта
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object

class ProductCreateView(CreateView):
    model = Product
    fields = ["name_product", "description", "image", "category", "price"]
    success_url = reverse_lazy("catalog:products_list")

class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name_product", "description", "image", "category", "price"]
    success_url = reverse_lazy("catalog:products_list")


    def get_success_url(self):
        return reverse('catalog:products_detail', args=[self.kwargs.get('pk')])

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:products_list")

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
