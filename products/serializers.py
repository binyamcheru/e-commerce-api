
from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'category', 'image', 'stock', 'available', 'average_rating')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'category', 'image', 'stock', 'available', 'average_rating', 'reviews')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'product', 'user', 'rating', 'comment', 'created_at')
        read_only_fields = ('user', 'product', 'created_at')
