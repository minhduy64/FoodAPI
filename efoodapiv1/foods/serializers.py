from rest_framework import serializers
from foods.models import Category, Store, MenuItem, Tag, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'image', 'created_date']
