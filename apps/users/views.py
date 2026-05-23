from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


def register_view(request):
    """Register a new student account."""
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('scholarships:list')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Login for both student and admin."""
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        if user.role == 'admin':
            return redirect('scholarships:admin_list')
        return redirect('scholarships:list')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Logout any user."""
    logout(request)
    return redirect('users:login')


@login_required
def profile_view(request):
    """View and edit own profile."""
    user = request.user
    if request.method == 'POST':
        user.name  = request.POST.get('name', user.name)
        user.phone = request.POST.get('phone', user.phone)
        user.save()
        return redirect('users:profile')
    return render(request, 'users/profile.html', {'user': user})