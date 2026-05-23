from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import CustomUser
from .models import Scholarship
import datetime


class ScholarshipTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = CustomUser.objects.create_user(
            email='admin@test.com', name='Admin', password='pass1234', role='admin'
        )
        self.student = CustomUser.objects.create_user(
            email='student@test.com', name='Student', password='pass1234', role='student'
        )
        self.scholarship = Scholarship.objects.create(
            name='Test Scholarship', provider='Binus', deadline=datetime.date(2026, 12, 31),
            country='Indonesia', level='s1', requirements='GPA 3.0',
            benefits='Full tuition', created_by=self.admin
        )

    def test_student_can_see_list(self):
        self.client.login(username='student@test.com', password='pass1234')
        res = self.client.get(reverse('scholarships:list'))
        self.assertEqual(res.status_code, 200)

    def test_admin_can_create(self):
        self.client.login(username='admin@test.com', password='pass1234')
        res = self.client.post(reverse('scholarships:create'), {
            'name': 'New Scholarship', 'provider': 'Gov',
            'deadline': '2026-12-31', 'country': 'Indonesia',
            'level': 's1', 'requirements': 'GPA 3.5', 'benefits': 'Monthly stipend'
        })
        self.assertEqual(Scholarship.objects.count(), 2)

    def test_search_filter(self):
        self.client.login(username='student@test.com', password='pass1234')
        res = self.client.get(reverse('scholarships:list') + '?q=Test')
        self.assertContains(res, 'Test Scholarship')