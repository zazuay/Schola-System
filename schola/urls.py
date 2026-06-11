from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/auth/login/')),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.urls', namespace='users')),
    path('scholarships/', include('apps.scholarships.urls', namespace='scholarships')),
    path('applications/', include('apps.applications.urls', namespace='applications')),
    path('resources/', include('apps.resources.urls', namespace='resources')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)