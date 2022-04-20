import json

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers import OrderCreateSerializer, SubOrderSerializer
from utils.helpers import get_local_datetime


class OrderView(APIView):

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.filter(customer=request.user)\
                              .order_by('-created_at')\
                              .prefetch_related('suborders')

        all_orders = []
        for order in orders:
            suborder_serializer = SubOrderSerializer(order.suborders, many=True)
            order_detail = {
                "order_id": order.order_id,
                "created_at": get_local_datetime(order.created_at),
                "total_amount": order.amount,
                "suborders": suborder_serializer.data
            }

            all_orders.append(order_detail)

        data = {
            "msg": "Order list fetched successfully." if all_orders else "Empty order list.",
            "order_details": all_orders
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)

    def post(self, request: HttpRequest) -> JsonResponse:
        paylaod = {
            "products": json.loads(request.POST.dict().get('products'))
        }

        order_serializer = OrderCreateSerializer(data=paylaod, context={'user': request.user})
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()
        data = {
            "msg": "Order placed successfully.",
            "order_id": order.order_id
        }
        return JsonResponse(status=status.HTTP_201_CREATED, data=data)
