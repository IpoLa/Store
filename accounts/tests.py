from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your tests here.
# TDD
User = get_user_model()
class UserTestCase(TestCase):

    def setUp(self):  # Python bultin's unittest
        user_a = User(username='rama', email='ipola@gmail.com')
        # User.objects.create()
        # User.objects.create_user()
        user_a_pw = 'abc123'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.save()
        user_a.set_password(user_a_pw)
        self.user_a = user_a
    
    def test_user_exists(self):
        user_count = User.objects.all().count()
        print(user_count)
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        # user_qs = User.objects.filter(username__iexact='rama')
        # user_exists = user_qs.exists() and user_qs.count() == 1
        # self.assertTrue(user_exists)
        # user_a = user_qs.first()
        self.assertTrue(
            self.user_a.check_password(self.user_a_pw)
        )

    def test_login_url(self):
        # login_url = "/login/"
        # self.assertEqual(settings.LOGIN_URL, login_url)
        login_url = settings.LOGIN_URL
        # Python requests - manage.py runserver
        # self.client.get, self.client.post
        # response = self.client.post(url, {}, follow=True)
        data = {"username": "rama", "password": self.user_a_pw}
        response = self.client.post(login_url, data, follow=True)
        # print(dir(response))
        print(response.request)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        # self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(status_code, 200)
