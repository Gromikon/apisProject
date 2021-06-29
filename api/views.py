from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotAcceptable
from rest_framework.filters import SearchFilter
from django.shortcuts import redirect
from .models import Order, Product
from .serializers import OrderSerializer, OrderUpdateSerializer, ProductSerializer

def redirect_view(request):
    response = redirect('api/v1/')
    return response

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter]
    filterset_fields = ['external_id', 'status', ]

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        if (order.status == 'accepted'):
            raise NotAcceptable('Status is already accepted')
        else:
            order.status = 'accepted'
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def fail(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        if (order.status == 'rejected'):
            raise NotAcceptable('Status is already rejected')
        else:
            order.status = 'rejected'
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_details = serializer.validated_data.get('details')
        try:
            product_data = order_details[0]
        except IndexError:
            raise NotAcceptable('Information about product is needed')
        user_given_product = product_data.get('product')
        user_product_id = user_given_product.get('id')
        if not Product.objects.filter(id=user_product_id).exists():
            raise ValidationError('Product doesn\'t exist')
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs.get('pk'))
        if order.status != 'new':
            raise ValidationError('Status can only be new')
        else:
            order.external_id = self.kwargs.get('external_id', order.external_id)
            serializer = OrderUpdateSerializer(instance=order,data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status == 'accepted':
            raise NotAcceptable('Accepted orders cannot be removed')
        else:
            return super(OrderViewSet, self).destroy(request, *args, **kwargs)
