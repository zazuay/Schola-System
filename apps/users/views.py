from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from .profile_forms import ProfileForm


def register_view(request):
    """Register a new student account."""
    form = RegisterForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('scholarships:list')
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(
            request,
            'Account created successfully.'
        )
        return redirect('scholarships:list')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Login for both student and admin."""
    form = LoginForm(request, data=request.POST or None)
    if request.user.is_authenticated:
        return redirect('scholarships:list')
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(
            request,
            f'Welcome back, {user.name}!'
        )
        if user.role == 'admin':
            return redirect('scholarships:admin_list')
        return redirect('scholarships:list')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Logout any user."""
    logout(request)
    messages.success(
        request,
        'You have been logged out.'
    )
    return redirect('users:login')


@login_required
def profile_view(request):
    form = ProfileForm(
        request.POST or None,
        instance=request.user
    )

    if request.method == 'POST' and form.is_valid():
        form.save()

        messages.success(
            request,
            'Profile updated.'
        )

        return redirect('users:profile')

    return render(
        request,
        'users/profile.html',
        {
            'form': form
        }
    )