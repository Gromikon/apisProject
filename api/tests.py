from django.urls import reverse
from django.test import TestCase
from .models import Order, Product, OrderDetail
from rest_framework import status
from rest_framework.test import APITestCase

class OrderTests(APITestCase):

    def setUp(self):

        self.order = Order.objects.create(
            status="new",
        )

        self.product = Product.objects.create(name="Name")
        #self.detail = OrderDetail.objects.create(product=self.product, order=self.order, amount=111, price=222)

        self.prod = Product.objects.create(
            name="megaproduct"
        )

    def test_post_order_details(self):
        response = self.client.post(
            reverse("details"), {
            				"order": self.order.id, 
                            "product": self.prod.id,
                            "amount": 110,
                            "price": 112
                               }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("product"), self.prod.id)

    def test_order_list(self):
        response = self.client.get(reverse("orders"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_exist_order(self):
        response = self.client.get(reverse("order_id", kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("status"), "new")

    def test_not_exist_order(self):
        response = self.client.get(reverse("order_id", kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
