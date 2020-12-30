from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Product

# Create your tests here.
User = get_user_model()

class ProductTestCase(TestCase):

    def setUp(self):
        user_a = User(username='rama', email='ipola@gmail.com')
        # User.objects.create()
        # User.objects.create_user()
        user_a_pw = 'abc123'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
        user_b = User.objects.create_user('user_2', 'ipola2@gmail.com', 'some_123_password')
        self.user_b = user_b

    def test_user_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_invalid_request(self):
        self.client.login(username=self.user_b.username, password='some_123_password')
        response = self.client.post("/products/create/", {"title": "this is a valid test"})
        # self.assertTrue(response.status_code!=200)  # 201
        self.assertNotEqual(response.status_code, 200)

    def test_valid_request(self):
        self.client.login(username=self.user_a.username, password='some_123_password')
        response = self.client.post("/products/create/", {"title": "this is a valid test"})
        # self.assertTrue(response.status_code == 200)  # 201
        self.assertNotEqual(response.status_code, 200)

    def test_product_created(self):
        product_obj = Product.objects.create(title="avc", content="My product", user=self.user_b)
        self.assertEqual(product_obj.id, 1)
        self.assertEqual(product_obj.user, self.user_b)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user_b.username, password='somepassword')
        return client

    def test_product_list(self):
        client = self.get_client()
        response = client.get("/products/")
        self.assertEqual(response.status_code, 200)
        print(len(response.json()), 3)

    def test_product_action(self):
        client = self.get_client()
        response = client.post("/api/products/action/", 
            {"id": 1, "action": "like"})
        # self.assertEqual(response.status_code, 200)
        print(response.json())
        # self.assertEqual(len(response.json()), 3)

    def test_product_detail_api_view(self):
        # request_data = {"content": "This is my test product"}
        client = self.get_client()
        response = client.get("/products/3/")
        # self.assertEqual(response.status_code, 200)
        data= response.json()
        _id = data.get("id")
        self.assertEqual(_id, 3)
        