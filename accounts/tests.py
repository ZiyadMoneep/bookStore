from django.test import TestCase
from django.contrib.auth import get_user_model
from http import HTTPStatus
from django.urls import reverse, resolve
from .views import SignUpView
from accounts.forms import CustomUserCreationForm


class CustomUserTests(TestCase):

    def test_userCreation(self):
        User = get_user_model()
        User = User.objects.create_user(
            username='zezo',
            email= 'zezo@gmail.com',
            age = '28',
            password='test@123'
        )
        self.assertEqual(User.username, 'zezo')
        self.assertEqual(User.email, 'zezo@gmail.com')
        self.assertEqual(User.age, '28')
        self.assertTrue(User.is_active)
        self.assertFalse(User.is_staff)
        self.assertFalse(User.is_superuser)

    def test_adminCreation(self):
        User = get_user_model()
        adminUser = User.objects.create_superuser(
            username='adminzezo',
            email='adminzezo@gmail.com',
            age='28',
            password='test@123'
        )
        self.assertEqual(adminUser.username, 'adminzezo')
        self.assertEqual(adminUser.email, 'adminzezo@gmail.com')
        self.assertEqual(adminUser.age, '28')
        self.assertTrue(adminUser.is_active)
        self.assertTrue(adminUser.is_staff)
        self.assertTrue(adminUser.is_superuser)


# class SignUpPageTest(TestCase):
#
#     def setUp(self):
#         url = reverse('accounts:signup')
#         self.response = self.client.get(url)
#
#     def test_Signup_template(self):
#         self.assertEqual(self.response.status_code, HTTPStatus.OK)
#         self.assertTemplateUsed(self.response, 'registration/signup.html')
#         self.assertContains(self.response, 'Sign Up')
#         self.assertNotContains(self.response, "Hello, You Should not be here")
#
#     def test_Signup_form(self):
#         form = self.response.context.get('form')
#         self.assertIsInstance(form, CustomUserCreationForm)
#         self.assertContains(self.response, 'csrfmiddlewaretoken')
#         self.assertNotContains(self.response, "Hello, You Should not be here")
#
#     def test_signUp_url_resolve_SignUpView(self):
#         view = resolve('/accounts/signup/')
#         self.assertEqual(view.func.__name__, SignUpView.as_view().__name__)


class SignUpPageTest(TestCase):

    username = 'testZ'
    email = 'testZ@example.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_Signup_template(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, "Hello, You Should not be here")

    def test_Signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)


