import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schola.settings')
django.setup()

from apps.users.models import CustomUser
from apps.scholarships.models import Scholarship
import datetime

admin = CustomUser.objects.create_user(email='admin@schola.com', name='Admin', password='admin123', role='admin')
CustomUser.objects.create_user(email='student@schola.com', name='Budi', password='student123', role='student')
Scholarship.objects.create(
    name='Beasiswa Unggulan Kemendikbud', provider='Kemendikbud',
    deadline=datetime.date(2026, 9, 30), country='Indonesia', level='s1',
    requirements='IPK min 3.00, aktif organisasi', benefits='SPP + uang saku Rp 2jt/bulan',
    created_by=admin
)
print("Seed done!")