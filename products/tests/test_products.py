from django.test import TestCase
from django.urls import reverse
from products.models import Product


class ProductViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(name="Test Product", price=10.00, quantity=5)

    def test_product_list_view_success(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_create_view_success(self):
        response = self.client.post(reverse('product_create'), {'name': 'New Product', 'price': 20.00, 'quantity': 10}, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_product_view_success(self):
        response = self.client.get(reverse('get_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_product_view_success(self):
        response = self.client.put(reverse('update_product', args=[self.product.pk]), {'name': 'Updated Product', 'price': 15.00, 'quantity': 8}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_product_view_success(self):
        response = self.client.delete(reverse('delete_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 204)
