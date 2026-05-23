from django.db import models
from django.conf import settings

class Scholarship(models.Model):
    LEVEL_CHOICES = [
        ('s1', 'S1 / Undergraduate'),
        ('s2', 'S2 / Master'),
        ('s3', 'S3 / Doctoral'),
    ]

    name         = models.CharField(max_length=255)
    provider     = models.CharField(max_length=255)
    deadline     = models.DateField()
    country      = models.CharField(max_length=100)
    level        = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    requirements = models.TextField()
    benefits     = models.TextField()
    created_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='scholarships_created'
    )
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name