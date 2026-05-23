from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import CustomUser
from apps.scholarships.models import Scholarship
from .models import Application
import datetime


class ApplicationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = CustomUser.objects.create_user(
            email='s@test.com', name='Student', password='pass', role='student'
        )
        self.admin = CustomUser.objects.create_user(
            email='a@test.com', name='Admin', password='pass', role='admin'
        )
        self.scholarship = Scholarship.objects.create(
            name='S1', provider='P', deadline=datetime.date(2026, 12, 31),
            country='ID', level='s1', requirements='R', benefits='B', created_by=self.admin
        )

    def test_student_can_apply(self):
        self.client.login(username='s@test.com', password='pass')
        self.client.post(reverse('applications:apply', kwargs={'scholarship_pk': self.scholarship.pk}))
        self.assertEqual(Application.objects.count(), 1)

    def test_one_apply_rule(self):
        self.client.login(username='s@test.com', password='pass')
        url = reverse('applications:apply', kwargs={'scholarship_pk': self.scholarship.pk})
        self.client.post(url)
        self.client.post(url, follow=True)  # second apply — should be silently blocked
        self.assertEqual(Application.objects.count(), 1)  # still only 1

    def test_admin_can_update_status(self):
        app = Application.objects.create(user=self.student, scholarship=self.scholarship)
        self.client.login(username='a@test.com', password='pass')
        self.client.post(
            reverse('applications:update_status', kwargs={'pk': app.pk}),
            {'status': 'accepted'}
        )
        app.refresh_from_db()
        self.assertEqual(app.status, 'accepted')