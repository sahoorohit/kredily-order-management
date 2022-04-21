from django.db import transaction
from rest_framework import serializers

from orders.models import Order, SubOrder
from products.models import Product


class OrderCreateProductSerializer(serializers.Serializer):
    product_id = serializers.CharField(required=True)
    quantity = serializers.IntegerField(default=1, required=False, min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    products = serializers.ListField(child=OrderCreateProductSerializer())

    def validate(self, attrs):
        products = attrs.get('products')

        errors = []
        for product in products:
            product_id = product.get('product_id')
            quantity = product.get('quantity')

            product_obj = Product.objects.filter(product_id=product_id).first()
            if product_obj:
                if product_obj.available_quantity < quantity:
                    errors.append({"quantity": f"{quantity} items for {product_id} is not available."})
            else:
                errors.append({"product_id": f"Invalid Product ID - {product_id}."})

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        products = validated_data.get('products')

        with transaction.atomic():
            order = Order.objects.create(customer=self.context['user'])
            total_order_amount = 0

            for product in products:
                product_obj = Product.objects.get(product_id=product.get('product_id'))

                quantity = product.get('quantity')
                suborder_amount = product_obj.price * quantity
                total_order_amount += suborder_amount

                SubOrder.objects.create(
                    item_name=product_obj.name,
                    unit_price=product_obj.price,
                    quantity=quantity,
                    amount=suborder_amount,
                    order=order
                )

                product_obj.available_quantity -= quantity
                product_obj.save()

            order.amount = total_order_amount
            order.save()

            return order


class SubOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubOrder
        fields = (
            'item_name',
            'unit_price',
            'quantity',
            'amount',
        )
