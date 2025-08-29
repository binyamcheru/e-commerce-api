from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ProductViewSet, CategoryViewSet, ReviewViewSet

# Main router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

# Nested router for products -> reviews
products_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
products_router.register(r'reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]