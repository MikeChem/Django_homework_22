from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            subject = 'Welcome!'
            html_message = render_to_string('users/welcome_email.html', {'user': user})
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            send_mail(subject, plain_message, from_email, to_email, html_message=html_message, fail_silently=False)

            messages.success(request, 'Registration successful! Welcome!')
            return redirect('product_list')
        else:
            messages.error(request, 'Registration error. Please check the data.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Получаем email из формы
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)  # Исправлено: username=email
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Login successful!')
                return redirect('product_list')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('product_list')
# Create your views here.
