from rest_framework import viewsets, generics
from foods.models import Category, Store
from foods import serializers, paginators


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class StoreViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Store.objects.filter(active=True)
    serializer_class = serializers.StoreSerializer
    pagination_class = paginators.StorePaginator
