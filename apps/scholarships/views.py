from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Scholarship
from .forms import ScholarshipForm
from apps.utils.decorators import admin_required
from apps.applications.models import Application


@login_required
def scholarship_list(request):
    """Student: browse all scholarships with optional search & filter."""
    qs = Scholarship.objects.all().order_by('-created_at')

    q = request.GET.get('q', '')
    country = request.GET.get('country', '')
    level = request.GET.get('level', '')

    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(provider__icontains=q)

    if country:
        qs = qs.filter(country__icontains=country)

    if level:
        qs = qs.filter(level=level)

    countries = Scholarship.objects.values_list(
        'country', flat=True
    ).distinct()

    return render(request, 'scholarships/list.html', {
        'scholarships': qs,
        'q': q,
        'countries': countries,
    })


@login_required
def scholarship_detail(request, pk):
    """Student: view single scholarship detail."""
    scholarship = get_object_or_404(Scholarship, pk=pk)

    already_applied = Application.objects.filter(
        user=request.user,
        scholarship=scholarship
    ).exists()

    return render(request, 'scholarships/detail.html', {
        'scholarship': scholarship,
        'already_applied': already_applied,
    })


# ---------- Admin Views ----------

@admin_required
def admin_scholarship_list(request):
    """Admin: see all scholarships they manage."""
    scholarships = Scholarship.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    return render(
        request,
        'scholarships/admin_list.html',
        {'scholarships': scholarships}
    )


@admin_required
def scholarship_create(request):
    """Admin: create new scholarship."""
    form = ScholarshipForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        scholarship = form.save(commit=False)
        scholarship.created_by = request.user
        scholarship.save()

        return redirect('scholarships:admin_list')

    return render(request, 'scholarships/form.html', {
        'form': form,
        'action': 'Create',
    })


@admin_required
def scholarship_edit(request, pk):
    """Admin: edit existing scholarship."""
    scholarship = get_object_or_404(Scholarship, pk=pk)

    form = ScholarshipForm(
        request.POST or None,
        instance=scholarship
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('scholarships:admin_list')

    return render(request, 'scholarships/form.html', {
        'form': form,
        'action': 'Edit',
    })


@admin_required
def scholarship_delete(request, pk):
    """Admin: delete scholarship."""
    scholarship = get_object_or_404(Scholarship, pk=pk)

    if request.method == 'POST':
        scholarship.delete()
        return redirect('scholarships:admin_list')

    return render(request, 'scholarships/confirm_delete.html', {
        'scholarship': scholarship,
    })