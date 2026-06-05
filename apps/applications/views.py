from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError, transaction

from .models import Application, Document
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
        doc = form.save(commit=False)
        doc.application = application
        doc.file_size = form.cleaned_data['file'].size
        doc.save()

        messages.success(request, 'Document uploaded.')

        return redirect(
            'applications:upload',
            application_pk=application.pk
        )

    documents = application.documents.all()

    return render(request, 'applications/upload.html', {
        'form': form,
        'application': application,
        'documents': documents,
    })


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


# ---------- Admin Views ----------

@admin_required
def applicant_list(request):
    """Admin: view all applications across all scholarships."""
    applications = (
        Application.objects
        .select_related('user', 'scholarship')
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
    application = get_object_or_404(Application, pk=pk)

    return render(
        request,
        'applications/admin_detail.html',
        {'application': application}
    )


@admin_required
def update_status_view(request, pk):
    """Admin: update application status (accept/reject)."""
    application = get_object_or_404(Application, pk=pk)

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