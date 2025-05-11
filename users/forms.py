from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)  # Только поле email
        error_messages = {
            'email': {'unique': "Этот email уже зарегистрирован."},
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Email", max_length=254)

    class Meta:
        model = User
        fields = ('email', 'password')