from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from decimal import Decimal

from .models import Product, Order


class CheckoutTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('9.99'),
            description='This is a test product.'
        )

    def test_checkout_process(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Add the product to the user's shopping cart
        self.client.post(reverse('add_to_cart', args=[self.product.id]))

        # Retrieve the shopping cart
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)

        # Check that the shopping cart contains the correct product
        self.assertContains(response, self.product.name)

        # Proceed to the checkout
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

        # Submit the order
        response = self.client.post(reverse('checkout'), {'payment_method': 'stripe'})
        self.assertEqual(response.status_code, 302)

        # Check that the order has been created
        orders = Order.objects.filter(user=self.user)
        self.assertEqual(orders.count(), 1)
        order = orders.first()

        # Check that the order total is correct
        self.assertEqual(order.total, self.product.price)

        # Check that a success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Order placed successfully.')

        # Check that the shopping cart is now empty
        response = self.client.get(reverse('view_cart'))
        self.assertNotContains(response, self.product.name)