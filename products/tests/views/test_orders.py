from django.test import TestCase
from django.urls import reverse
from products.models import Product, Customer, Order
from django.utils import timezone
import json


class OrderViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = Customer.objects.create(name="Test Customer")
        cls.product = Product.objects.create(name="Test Product", price=19.99, quantity=10)

    def test_list_orders_success(self):
        Order.objects.create(customer=self.customer, product=self.product, price=19.99, quantity=1, datetime=timezone.now())

        response = self.client.get(reverse('list_orders', args=[self.customer.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.json())

    def test_create_order_success(self):
        order_data = {
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            'price': 19.99,
            'quantity': 1
        }
        response = self.client.post(reverse('create_order'),
                                    data=json.dumps(order_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Order.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 9)

