from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Product


class ProductTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_product_list_view(self):
        # Create some test products
        product1 = Product.objects.create(name='Product 1', price=10.99)
        product2 = Product.objects.create(name='Product 2', price=15.99)

        # Access the product list view
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

        # Check that both products are listed
        self.assertContains(response, product1.name)
        self.assertContains(response, product2.name)

    def test_product_detail_view(self):
        # Create a test product
        product = Product.objects.create(name='Test Product', price=9.99)

        # Access the product detail view
        response = self.client.get(reverse('product_detail', args=[product.id]))
        self.assertEqual(response.status_code, 200)

        # Check that the product details are displayed correctly
        self.assertContains(response, product.name)
        self.assertContains(response, product.price)

    def test_add_to_cart_view(self):
        # Create a test product
        product = Product.objects.create(name='Test Product', price=9.99)

        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Add the product to the user's shopping cart
        response = self.client.post(reverse('add_to_cart', args=[product.id]))
        self.assertEqual(response.status_code, 302)

        # Check that the product is added to the shopping cart
        self.assertEqual(len(self.client.session['cart']), 1)
        self.assertEqual(self.client.session['cart'][0]['product_id'], product.id)

    # Add more test cases as needed for other features of the products section

