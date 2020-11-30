from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your tests here.
# TDD
User = get_user_model()
class OrderTestCase(TestCase):

    def setUp(self):  # Python bultin's unittest
        user_a = User(username='rama', email='ipola@gmail.com')
        # User.objects.create()
        # User.objects.create_user()
        user_a_pw = 'some_123_password'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

    # def test_create_order(self):
    #     obj = Order.objects.create(user=self.user_a, product=product_a)