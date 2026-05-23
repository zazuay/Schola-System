from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def student_required(view_func):
    """Allow only authenticated students."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != 'student':
            messages.error(request, 'Access denied: students only.')
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Allow only authenticated admins."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != 'admin':
            messages.error(request, 'Access denied: admins only.')
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper