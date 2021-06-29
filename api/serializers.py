from rest_framework import serializers

from .models import Order, OrderDetail, Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'name']


class OrderDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ['id', 'product', 'amount', 'price']

    def create(self, validated_data):
        product = validated_data['product']
        order = validated_data['order']
        amount = validated_data['amount']
        price = validated_data['price']
        order_detail = OrderDetail()
        order_detail.price = price
        order_detail.amount = amount
        order_detail.product = product
        order_detail.order = order
        order_detail.save()
        return order_detail

    def update(self, instance, validated_data):
        product = validated_data['product']
        amount = validated_data['amount']
        price = validated_data['price']
        instance.amount = amount
        instance.price = price
        instance.save()
        return instance

class OrderUpdateSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'status', 'created_at', 'external_id', 'details']
        read_only_fields = ['id', 'status', 'created_at', 'details']

    def to_internal_value(self, data):
        in_data = {}
        for key, value in data.items():
            if key == 'external_id':
                in_data[key] = value
        return in_data


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'created_at', 'external_id', 'details']
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        details = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for detail in details:
            product_data = detail.pop('product')
            product, created = Product.objects.get_or_create(**product_data)
            OrderDetail.objects.create(**detail, order=order, product=product)
        return order
