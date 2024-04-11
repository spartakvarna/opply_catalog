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
        self.assertEqual(response.status_code, 200)

    def test_product_create_view_missing_parameters(self):
        response = self.client.post(reverse('product_create'), {'name': 'Incomplete Product'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_product_create_view_negative_price(self):
        response = self.client.post(reverse('product_create'), {'name': 'New Product', 'price': -20.00, 'quantity': 10}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_product_create_view_duplicate_name(self):
        response = self.client.post(reverse('product_create'), {'name': self.product.name, 'price': 20.00, 'quantity': 10}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_product_view_success(self):
        response = self.client.get(reverse('get_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_get_product_view_not_found(self):
        response = self.client.get(reverse('get_product', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_update_product_view_success(self):
        response = self.client.put(reverse('update_product', args=[self.product.pk]), {'name': 'Updated Product', 'price': 15.00, 'quantity': 8}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_product_view_not_found(self):
        response = self.client.put(reverse('update_product', args=[9999]), {'name': 'Updated Product', 'price': 15.00, 'quantity': 8}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_product_view_negative_price(self):
        response = self.client.put(reverse('update_product', args=[self.product.pk]), {'name': 'Updated Product', 'price': -15.00, 'quantity': 8}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_product_view_success(self):
        response = self.client.delete(reverse('delete_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_product_view_not_found(self):
        response = self.client.delete(reverse('delete_product', args=[9999]))  # Assuming ID 9999 does not exist
        self.assertEqual(response.status_code, 404)

    def test_soft_delete_product_success(self):
        self.client.post(reverse('soft_delete_product', args=[self.product.pk]))
        product = Product.objects.get(pk=self.product.pk)
        self.assertIsNotNone(product.deleted_at)

    def test_soft_delete_product_not_found(self):
        response = self.client.post(reverse('soft_delete_product', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_enable_product_success(self):
        self.product.is_active = False
        self.product.save()
        response = self.client.post(reverse('enable_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Product.objects.get(pk=self.product.pk).is_active)

    def test_enable_product_not_found(self):
        response = self.client.post(reverse('enable_product', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_disable_product_success(self):
        response = self.client.post(reverse('disable_product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.get(pk=self.product.pk).is_active)

    def test_disable_product_not_found(self):
        response = self.client.post(reverse('disable_product', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_toggle_product_enabled_success(self):
        initial_state = self.product.is_active
        response = self.client.post(reverse('toggle_product_enabled', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Product.objects.get(pk=self.product.pk).is_active, initial_state)

    def test_toggle_product_enabled_not_found(self):
        response = self.client.post(reverse('toggle_product_enabled', args=[9999]))
        self.assertEqual(response.status_code, 404)
