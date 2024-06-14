from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from foods import views


r = routers.DefaultRouter()
r.register('categories', views.CategoryViewSet, 'categories')
r.register('stores', views.StoreViewSet, 'stores')
r.register('menu_items', views.MenuItemViewSet, 'menu_items')
r.register('users', views.UserViewSet, 'users')
r.register('comments', views.CommentViewSet, 'comments')
urlpatterns = [
    path('', include(r.urls))
]
