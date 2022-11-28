from django.test import TestCase
from django.urls import reverse

from customers.models import CustomerUser


class RegisterPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.page_name = reverse(viewname='register')
        cls.user = {
            'email': 'test5@test.com',
            'full_name': 'Test1',
            'phone_number': '89522611692',
            'password1': 'TestPass12',
            'password2': 'TestPass12'
        }
        cls.user_short_password = {
            'email': 'test5@test.com',
            'full_name': 'Test1',
            'phone_number': '89522611692',
            'password1': 'Test',
            'password2': 'Test'
        }
        cls.user_different_passwords = {
            'email': 'test5@test.com',
            'full_name': 'Test1',
            'phone_number': '89522611692',
            'password1': 'Test',
            'password2': 'Test1'
        }

    def setUp(self):
        self.get_response = self.client.get(self.page_name)

    def test_register_page(self):
        response = self.client.get(self.page_name)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.page_name, self.user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomerUser.objects.all().count(), 1)
        self.assertEqual(CustomerUser.objects.get(id=1).email, 'test5@test.com')

    def test_cant_register(self):
        response = self.client.post(self.page_name, self.user_short_password)
        self.assertNotEqual(response.status_code, 302)
        response = self.client.post(self.page_name, self.user_different_passwords)
        self.assertNotEqual(response.status_code, 302)

    def test_authenticated_after_register(self):
        self.client.post(self.page_name, self.user)
        response = self.client.get(self.page_name)



class LoginPageTest(TestCase):

    def setUp(self):
        self.page_name = reverse(viewname='login')
        test_user = CustomerUser.objects.create_user(email='testuser1',
                                                     full_name='Test1',
                                                     phone='89522611692',
                                                     password='TestPass12')
        test_user.save()

    def test_login_page(self):
        response = self.client.get(self.page_name)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/login.html')

    def test_login(self):
        response = self.client.post(self.page_name, {
            'email': 'test5@test.com',
            'password': 'TestPass12'
        })
        self.assertEqual(response.status_code, 200)
