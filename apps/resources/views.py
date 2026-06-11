from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def resources_view(request):
    """Student: main resource hub page (guides, templates, FAQs, etc.)."""
    return render(request, 'resources/resources.html', {
        'featured_articles': [],
        'templates': [],
        'faqs': [],
        'success_stories': [],
        'live_sessions': [],
    })


@login_required
def category_list_view(request):
    """Student: resource library / category overview page."""
    return render(request, 'resources/category_list.html')


@login_required
def article_detail_view(request, pk=None):
    """Student: view a single resource/article."""
    return render(request, 'resources/article_detail.html', {
        'article_pk': pk,
    })


@login_required
def download_template_view(request, pk):
    """Student: download a CV/document template (placeholder)."""
    messages.info(request, 'Template downloads are not available yet.')
    return redirect('resources:list')
