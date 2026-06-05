from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import RegisterForm, LoginForm


def _safe_next_url(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if (
        next_url
        and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
    ):
        return next_url
    return None


# 1. Регистрация
def register_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(_safe_next_url(request) or 'book_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# 2. Вход
def login_view(request):
    if request.user.is_authenticated:
        return redirect(_safe_next_url(request) or 'book_list')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(_safe_next_url(request) or 'book_list')
    else:
        form = LoginForm()

    return render(
        request,
        'registration/login.html',
        {
            'form': form,
            'next': request.POST.get('next', request.GET.get('next', '')),
        },
    )


# 3. Выход
def logout_view(request):
    logout(request)
    return redirect('book_list')


# 4. Профиль (Личный кабинет)
@login_required
def profile_view(request):
    return render(request, 'registration/profile.html')
