from rest_framework import serializers
from foods.models import Category, Store, MenuItem, Tag, User, Comment, Order


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url
        return req


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['icon'] = instance.icon.url
        return req


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class StoreSerializer(ItemSerializer):
    category_name = serializers.CharField(source='categories.name', read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'image', 'location', 'longitude', 'latitude', 'approved', 'category_name']


class MenuItemSerializer(ItemSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'image', 'created_date']


class MenuItemDetailSerializer(MenuItemSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = MenuItemSerializer.Meta.model
        fields = MenuItemSerializer.Meta.fields + ['tags', 'content']


class AuthenticatedMenuItemDetailSerializer(MenuItemDetailSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, menu_item):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return menu_item.likes.filter(active=True, user=request.user).exists()

    class Meta:
        model = MenuItemDetailSerializer.Meta.model
        fields = MenuItemDetailSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url

        return rep

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


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'user']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'store', 'menu_items', 'total_price']
