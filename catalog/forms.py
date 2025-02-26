from django import forms
from .models import Product
from django.core.exceptions import ValidationError

FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]

def contains_forbidden_words(value):
    """Проверяет, содержит ли строка запрещенные слова (без учета регистра)."""
    for word in FORBIDDEN_WORDS:
        if word.lower() in value.lower():
            raise ValidationError(f"Запрещено использовать слово '{word}'.")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['views_counter',]

    def clean_name_product(self):
        name = self.cleaned_data['name_product']
        try:
            contains_forbidden_words(name)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        try:
            contains_forbidden_words(description)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if int(price) < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Настройка атрибутов виджета для поля 'first_name'
        self.fields['name_product'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите название продукта'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'last_name'
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите описание'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'email'
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите категорию'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'enrollment_date'
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите цену'  # Указание типа поля как даты
        })

