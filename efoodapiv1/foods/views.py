from rest_framework import viewsets, generics, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from foods.models import Category, Store, MenuItem, User
from foods import serializers, paginators


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class StoreViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Store.objects.filter(active=True)
    serializer_class = serializers.StoreSerializer
    pagination_class = paginators.StorePaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action == 'list':
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            cate_id = self.request.query_params.get('categories_id')
            if cate_id:
                queryset = queryset.filter(categories_id=cate_id)

        return queryset

    @action(methods=['get'], url_path='menu_items', detail=True)
    def get_menu_items(self, request, pk):
        menu_items = self.get_object().menu_item_set.filter(active=True)
        return Response(serializers.MenuItemSerializer(menu_items, many=True).data,
                        status=status.HTTP_200_OK)


class MenuItemViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = MenuItem.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.MenuItemDetailSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    parser_classes = [parsers.MultiPartParser]