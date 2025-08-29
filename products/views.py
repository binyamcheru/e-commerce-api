from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, Review
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, ReviewSerializer
from accounts.permissions import GuestPermission, IsAdminOrSuperAdmin, IsCustomer, IsOwner

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrSuperAdmin]
        else:
            self.permission_classes = [GuestPermission]
        return super().get_permissions()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'average_rating']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrSuperAdmin]
        else:
            self.permission_classes = [GuestPermission]
        return super().get_permissions()

    @action(detail=True, methods=['get'], serializer_class=ReviewSerializer, permission_classes=[GuestPermission])
    def reviews(self, request, slug=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], serializer_class=ReviewSerializer, permission_classes=[IsCustomer])
    def add_review(self, request, slug=None):
        product = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"   # tells router to use slug instead of pk

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsCustomer]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsCustomer, IsOwner]
        else:
            self.permission_classes = [GuestPermission]
        return super().get_permissions()

    def perform_create(self, serializer):
        # For nested routes, product comes from URL parameter
        product_slug = self.kwargs.get('product_slug')
        if product_slug:
            try:
                product = Product.objects.get(slug=product_slug)
                serializer.save(user=self.request.user, product=product)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product": "Product not found."})
        else:
            # For flat routes, product should be in request data
            if 'product' not in serializer.validated_data:
                raise serializers.ValidationError({"product": "Product is required."})
            serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by product if using nested routing
        product_slug = self.kwargs.get('product_slug')
        if product_slug:
            queryset = queryset.filter(product__slug=product_slug)
        return queryset
