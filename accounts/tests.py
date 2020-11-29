from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
# TDD
User = get_user_model()
class UserTestCase(TestCase):

    def setUp(self):  # Python bultin's unittest
        user_a = User(username='rama', email='ipola@gmail.com')
        # User.objects.create()
        # User.objects.create_user()
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password('abc123')
        user_a.sava()
        print(user_a.id)