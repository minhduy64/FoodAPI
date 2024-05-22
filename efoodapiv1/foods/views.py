from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from foods.models import Category, Store, MenuItem, User, Comment, LikeMenuItem
from foods import serializers, paginators, perms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


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
        menu_items = self.get_object().menuitem_set.filter(active=True)

        q = request.query_params.get('q')
        if q:
            menu_items = menu_items.filter(subject__icontains=q)

        return Response(serializers.MenuItemSerializer(menu_items, many=True).data,
                        status=status.HTTP_200_OK)


class MenuItemViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = MenuItem.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.MenuItemDetailSerializer

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return serializers.AuthenticatedMenuItemDetailSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').all()
        paginator = paginators.CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializer(comments, many=True).data
                        , status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = self.get_object().comments.create(content=request.data.get('content'),
                                                 user=request.user)
        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], url_path='like', detail=True)
    def like(self, request, pk):
        li, created = LikeMenuItem.objects.get_or_create(menu_item=self.get_object(),
                                                         user=request.user)

        if not created:
            li.active = not li.active
            li.save()

        return Response(serializers.MenuItemSerializer(self.get_object()).data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.CommnetOwner]


@login_required
def follow_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.user in store.followers.all():
        store.followers.remove(request.user)
    else:
        store.followers.add(request.user)
    return redirect('store_detail', store_id=store_id)