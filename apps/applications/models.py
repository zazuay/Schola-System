from django.db import models
from django.conf import settings
from apps.scholarships.models import Scholarship

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    scholarship    = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_submitted = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'scholarship')  # one-apply rule

    def __str__(self):
        return f"{self.user.name} → {self.scholarship.name} [{self.status}]"


def upload_to(instance, filename):
    return f"documents/{instance.application.id}/{filename}"


class Document(models.Model):
    TYPE_CHOICES = [
        ('cv',                 'CV'),
        ('transcript',         'Transcript'),
        ('motivation_letter',  'Motivation Letter'),
    ]

    application  = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    type         = models.CharField(max_length=25, choices=TYPE_CHOICES)
    file         = models.FileField(upload_to=upload_to)
    file_size    = models.PositiveIntegerField(help_text='Size in bytes')
    uploaded_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} for App#{self.application.id}"