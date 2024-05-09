from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from foods import views


r = routers.DefaultRouter()
r.register('categories', views.CategoryViewSet, 'categories')
r.register('stores', views.StoreViewSet, 'stores')

urlpatterns = [
    path('', include(r.urls))
]
