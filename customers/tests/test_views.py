from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from customers.forms import ChangeUserData
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


class AccountPageTest(TestCase):
    def setUp(self):
        test_user = CustomerUser.objects.create(email='testuser1',
                                                full_name='Test1',
                                                phone='89522611692',
                                                password='TestPass12')
        self.user = test_user
        self.page_name = reverse(viewname='account')

    def test_account_page(self):
        response = self.client.get(self.page_name)
        self.assertEqual(response.status_code, 200)


class ProfilePageTest(TestCase):
    def setUp(self):
        test_user = CustomerUser.objects.create(email='testuser@mail.ru',
                                                full_name='Test1',
                                                phone='89522611692',
                                                password='TestPass12')
        self.user = test_user
        self.page_name = reverse(viewname='profile')
        self.form_data = {'full_name': 'TestUser',
                          'phone': '89522611693',
                          'email': 'test@t.ru',
                          'password': 'TestPass12',
                         }

    def test_profile_page(self):
        response = self.client.get(self.page_name)
        self.assertEqual(response.status_code, 200)

    def test_form_user_data(self):
        form = ChangeUserData(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_change_user_data(self):
        request = HttpRequest()
        request.POST = {'full_name': 'TestUser1',
                         'phone': '89522611693',
                         'email': 'test@t.ru',
                         'password': 'TestPass12',
                         }
        form = ChangeUserData(request.POST, instance=self.user)
        form.save()
        self.assertTrue(form.cleaned_data.get('full_name') == 'TestUser1')
