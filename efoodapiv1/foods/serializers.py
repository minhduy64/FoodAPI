from rest_framework import serializers
from foods.models import Category, Store, MenuItem, Tag, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url
        return req


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class StoreSerializer(ItemSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'image', 'created_date']


class MenuItemSerializer(ItemSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'image', 'created_date']


class MenuItemDetailSerializer(MenuItemSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = MenuItemSerializer.Meta.model
        fields = MenuItemSerializer.Meta.fields + ['content', 'tags']


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True}
        }