from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class Scholarship(models.Model):
    LEVEL_CHOICES = [
        ('s1', 'S1 / Undergraduate'),
        ('s2', 'S2 / Master'),
        ('s3', 'S3 / Doctoral'),
    ]

    name         = models.CharField(max_length=255, db_index=True)
    provider     = models.CharField(max_length=255, db_index=True)
    deadline     = models.DateField()
    country      = models.CharField(max_length=100, db_index=True)
    level        = models.CharField(max_length=10, choices=LEVEL_CHOICES, db_index=True)
    requirements = models.TextField()
    benefits     = models.TextField()
    created_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='scholarships_created'
    )
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def clean(self):
        # Added timezone.now().date() to ensure we compare date to date
        if self.deadline and self.deadline < timezone.now().date():
            raise ValidationError({
                'deadline': 'Deadline cannot be in the past.'
            })

    @property
    def is_open(self):
        if not self.deadline:
            return False
        return self.deadline >= timezone.now().date()