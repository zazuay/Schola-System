from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import CustomUser


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='student@test.com', name='Test Student', password='pass1234'
        )

    def test_register_get(self):
        res = self.client.get(reverse('users:register'))
        self.assertEqual(res.status_code, 200)

    def test_login_valid(self):
        res = self.client.post(reverse('users:login'), {
            'username': 'student@test.com', 'password': 'pass1234'
        })
        self.assertRedirects(res, reverse('scholarships:list'))

    def test_login_invalid(self):
        res = self.client.post(reverse('users:login'), {
            'username': 'student@test.com', 'password': 'wrongpass'
        })
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Please enter a correct')