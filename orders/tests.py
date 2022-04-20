import json
from typing import Tuple

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import User
from orders.models import Order, SubOrder
from products.models import Product
from products.tests import ProductTest


class OrderTest(APITestCase):

    def setUp(self) -> None:
        ProductTest().create_dummy_products()

        self.username = "john"
        self.password = "password"

        self.user = User.objects.create(username='testuser')
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    @property
    def url(self) -> str:
        return reverse('orders')

    def get_valid_product_details(self, instance_number: int) -> Tuple[str, int]:
        products = Product.objects.all()
        product = products[instance_number-1]
        return product.product_id, product.available_quantity

    def test_get_orders_when_user_not_logged_in__failure(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token Invalid-Token')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_when_user_has_no_previous_order_history__success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], "Empty order list.")
        self.assertEqual(len(response_body['order_details']), 0)

    def test_get_orders__success(self):
        self.test_create_order_with_multiple_product__success()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['msg'], "Order list fetched successfully.")
        self.assertEqual(len(response_body['order_details']), 1)
        self.assertEqual(len(response_body['order_details'][0]['suborders']), 2)

    def test_create_order_when_user_is_not_logged_in__failure(self):
        product_id, available_quantity = self.get_valid_product_details(1)
        payload = {
            "products": json.dumps([
                {"product_id": product_id, "quantity": available_quantity}
            ])
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token Invalid-Token')

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_when_product_id_is_invalid__failure(self):
        payload = {
            "products": json.dumps([
                {"product_id": "invalid-product-id", "quantity": 1}
            ])
        }

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_a_single_product_when_quantity_requested_is_more_than_availability__failure(self):
        product_id, available_quantity = self.get_valid_product_details(1)
        payload = {
            "products": json.dumps([
                {"product_id": product_id, "quantity": available_quantity + 1}
            ])
        }

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_a_single_product__success(self):
        product_id, available_quantity = self.get_valid_product_details(1)
        payload = {
            "products": json.dumps([
                {"product_id": product_id, "quantity": available_quantity}
            ])
        }

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        orders = Order.objects.all()
        self.assertEqual(len(orders), 1)

        suborders = SubOrder.objects.all()
        self.assertEqual(len(suborders), 1)

        product = Product.objects.get(product_id=product_id)
        self.assertEqual(product.available_quantity, 0)

    def test_create_order_with_multiple_product_when_quantity_requested_is_more_than_availability__failure(self):
        product_id, available_quantity = self.get_valid_product_details(1)
        product_id_2, available_quantity_2 = self.get_valid_product_details(2)
        payload = {
            "products": json.dumps([
                {"product_id": product_id, "quantity": available_quantity},
                {"product_id": product_id_2, "quantity": available_quantity_2 + 1}
            ])
        }

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_multiple_product__success(self):
        product_id, available_quantity = self.get_valid_product_details(1)
        product_id_2, available_quantity_2 = self.get_valid_product_details(2)
        payload = {
            "products": json.dumps([
                {"product_id": product_id, "quantity": available_quantity},
                {"product_id": product_id_2, "quantity": available_quantity_2}
            ])
        }

        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        orders = Order.objects.all()
        self.assertEqual(len(orders), 1)

        suborders = SubOrder.objects.all()
        self.assertEqual(len(suborders), 2)

        product = Product.objects.get(product_id=product_id)
        self.assertEqual(product.available_quantity, 0)

        product_2 = Product.objects.get(product_id=product_id_2)
        self.assertEqual(product_2.available_quantity, 0)
