from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm

# 1. Регистрация
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index') # или 'book_list'
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# 2. Вход
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# 3. Выход
def logout_view(request):
    logout(request)
    return redirect('index')

# 4. Профиль (Личный кабинет)
@login_required
def profile_view(request):
    return render(request, 'registration/profile.html')