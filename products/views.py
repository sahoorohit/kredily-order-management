from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductSerializer
from utils.helpers import get_paginated_objects


class ProductView(APIView):
    permission_classes = []

    DEFAULT_PAGINATED_ENTRIES = 10

    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.all().order_by('available_quantity')
        paginator = Paginator(products, self.DEFAULT_PAGINATED_ENTRIES)
        paginated_products = get_paginated_objects(paginator, request.GET.get('page'))

        product_serializer = ProductSerializer(paginated_products, many=True)
        data = {
            "msg": "Product list fetched successfully." if product_serializer.data else "Empty product list.",
            "products": product_serializer.data
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)
