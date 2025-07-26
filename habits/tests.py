from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
import uuid
from django.urls import reverse
from unittest.mock import patch
from .models import User, Habit, PasswordReset


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(
            name='Test User',
            email='test@example.com',
            date_of_birth=date(1990, 5, 15),
            password=make_password('securepassword'),
            role='Developer'
        )
        self.assertEqual(user.name, 'Test User')


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name='Habit User',
            email='habit@example.com',
            date_of_birth=date(1995, 10, 20),
            password=make_password('habitpass'),
            role='Developer'
        )

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            name='Morning Run',
            description='Run for 30 minutes',
            duration=timedelta(minutes=30)
        )
        self.assertEqual(habit.user, self.user)


class PasswordResetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            date_of_birth=date(1990, 1, 1),
            password=make_password('testpass'),
            role='Developer'
        )

    def test_password_reset_creation(self):
        reset = PasswordReset.objects.create(user=self.user)
        self.assertEqual(reset.user, self.user)
        self.assertIsInstance(reset.reset_id, uuid.UUID)


class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            date_of_birth=date(1990, 1, 1),
            password=make_password('testpass'),
            role='Developer'
        )

    def test_login_success(self):
        response = self.client.post('/login/', {
            'username': 'Test User',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_failure(self):
        response = self.client.post('/login/', {
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)


class PasswordResetViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            date_of_birth=date(1990, 1, 1),
            password=make_password('testpass'),
            role='Developer'
        )

    @patch('django.core.mail.EmailMessage.send')  # <- fixed here
    def test_forgot_password(self, mock_send):
        response = self.client.post('/forgot-password/', {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        mock_send.assert_called_once()

    def test_reset_password_page(self):
        reset = PasswordReset.objects.create(user=self.user)
        response = self.client.get(f'/reset-password/{reset.reset_id}/')
        self.assertEqual(response.status_code, 200)


class HabitManagementViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            date_of_birth=date(1990, 1, 1),
            password=make_password('testpass'),
            role='Developer'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            description='Test Description',
            duration=timedelta(hours=1)
        )
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

    def test_habit_list(self):
        response = self.client.get('/')  # home page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.habit.name)

    def test_habit_detail(self):
        response = self.client.get(f'/Habit/{self.habit.id}/')  # fixed URL
        self.assertEqual(response.status_code, 200)

    def test_create_habit(self):
        response = self.client.post('/create-habit/', {
            'user': self.user.id,
            'name': 'New Habit',
            'description': 'New Description',
            'duration': '01:00:00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Habit.objects.filter(name='New Habit').exists())

    def test_delete_habit(self):
        response = self.client.post(f'/delete-habit/{self.habit.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())
