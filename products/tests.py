import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from products.models import Product
from products.views import ProductView


class ProductTest(TestCase):

    def setUp(self) -> None:
        for i in range(1, 15):
            Product.objects.create(name=f"Product Name {i}", price=100 * i, available_quantity=2 * i)

    @property
    def url(self) -> str:
        return reverse('products')

    def assert_success_response(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Product list fetched successfully.')
        self.assertEqual(len(response_body['products']), ProductView().DEFAULT_PAGINATED_ENTRIES)

        self.assertIsNotNone(response_body['products'][0]['product_id'])
        self.assertIsNotNone(response_body['products'][0]['name'])
        self.assertIsNotNone(response_body['products'][0]['price'])
        self.assertIsNotNone(response_body['products'][0]['available_quantity'])

    def test_get_product_list_when_page_number_not_passed_in_query_param(self):
        response = self.client.get(self.url)
        self.assert_success_response(response=response)

    def test_get_product_list_when_page_number_is_not_an_integer(self):
        response = self.client.get(f'{self.url}?page=invalid-page-number')
        self.assert_success_response(response=response)

    def test_get_product_list_when_page_number_provided_is_an_integer(self):
        response = self.client.get(f'{self.url}?page=1')
        self.assert_success_response(response=response)

    def test_get_product_list_when_no_product_left_for_pagination(self):
        response = self.client.get(f'{self.url}?page=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], 'Empty product list.')
        self.assertEqual(len(response_body['products']), 0)
