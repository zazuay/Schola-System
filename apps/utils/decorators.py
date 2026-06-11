from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def student_required(view_func):
    """Allow only authenticated students."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != request.user.STUDENT:
            messages.error(
                request,
                'Access denied.'
            )
            return redirect('users:profile')
        if not request.user.is_active:
            messages.error(
                request,
                'Account disabled.'
            )
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Allow only authenticated admins."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != request.user.ADMIN:
            messages.error(
                request,
                'Access denied.'
            )

            return redirect('users:profile')
        if not request.user.is_active:
            messages.error(
                request,
                'Account disabled.'
            )
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper