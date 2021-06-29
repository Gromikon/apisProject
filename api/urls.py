from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/v1/orders', views.OrderViewSet, basename='orders')
router.register(r'api/v1/products', views.ProductViewSet, basename='products')

urlpatterns = [
	path("", include(router.urls)),
    path("api/v1/orders/", views.OrderViewSet, name="orders"),
    path("api/v1/products/", views.ProductViewSet, name="products")
]
