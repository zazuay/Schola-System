from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError, transaction
import datetime # Added for the mock notification logic

from .models import Application, Document, Notification
from .forms import ApplicationForm, DocumentForm
from apps.scholarships.models import Scholarship
from apps.utils.decorators import student_required, admin_required


@student_required
def apply_view(request, scholarship_pk):
    """Student: apply for a scholarship."""
    scholarship = get_object_or_404(Scholarship, pk=scholarship_pk)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                Application.objects.create(
                    user=request.user,
                    scholarship=scholarship
                )

                Notification.objects.create(
                    user=request.user,
                    type='success',
                    title='Application Submitted',
                    message=f'Your application for {scholarship.name} has been submitted.'
                )

            messages.success(request, 'Application submitted!')
            return redirect('applications:status')

        except IntegrityError:
            messages.error(
                request,
                'You have already applied for this scholarship.'
            )

    return render(
        request,
        'applications/apply_confirm.html',
        {'scholarship': scholarship}
    )


@student_required
def upload_view(request, application_pk):
    """Student: upload documents for an application."""
    application = get_object_or_404(
        Application,
        pk=application_pk,
        user=request.user
    )

    form = DocumentForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == 'POST' and form.is_valid():
        try:
            doc = form.save(commit=False)
            doc.application = application
            doc.save()

            messages.success(
                request,
                'Document uploaded successfully.'
            )

            return redirect(
                'applications:upload',
                application_pk=application.pk
            )

        except IntegrityError:
            messages.error(
                request,
                'You already uploaded this document type.'
            )


@student_required
def status_view(request):
    applications = Application.objects.filter(user=request.user).select_related('scholarship')
    pending_count  = applications.filter(status='pending').count()
    accepted_count = applications.filter(status='accepted').count()
    rejected_count = applications.filter(status='rejected').count()
    return render(request, 'applications/status.html', {
        'applications': applications,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
    })

# --- NEW VIEW ADDED HERE ---
@student_required
def notifications_view(request):
    notifications = request.user.notifications.all()

    return render(
        request,
        'applications/notifications.html',
        {
            'notifications': notifications
        }
    )

@student_required
def mark_all_read_view(request):
    """Student: Mark all notifications as read (Dummy endpoint for now)"""
    if request.method == 'POST':
        request.user.notificatiions.update(
            is_read = True
        )
    
    return redirect('applications:notifications')

# --- END NEW VIEW ---


# ---------- Admin Views ----------

@admin_required
def applicant_list(request):
    """Admin: view all applications across all scholarships."""
    applications = (
        Application.objects
        .select_related('user', 'scholarship')
        .filter(
            scholarship__created_by=request.user
        )
        .order_by('-date_submitted')
    )

    return render(request, 'applications/admin_list.html', {
        'applications': applications,
        'pending_count': applications.filter(status='pending').count(),
        'accepted_count': applications.filter(status='accepted').count(),
        'rejected_count': applications.filter(status='rejected').count(),
    })


@admin_required
def applicant_detail(request, pk):
    """Admin: view detail of one application including uploaded docs."""
    application = get_object_or_404(Application, pk=pk, scholarship__created_by=request.user)

    return render(
        request,
        'applications/admin_detail.html',
        {'application': application}
    )


@admin_required
def update_status_view(request, pk):
    """Admin: update application status (accept/reject)."""
    application = get_object_or_404(Application, pk=pk, scholarship__created_by=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['pending', 'accepted', 'rejected']:
            application.status = new_status
            application.save()

            messages.success(
                request,
                f'Status updated to {new_status}.'
            )

        return redirect(
            'applications:admin_detail',
            pk=pk
        )

    return redirect('applications:admin_list')