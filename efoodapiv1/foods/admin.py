from django.contrib import admin
from django.utils.html import mark_safe
from foods.models import Store, Category, MenuItem, Tag, Comment, ReviewStore, ReviewMenuItem, Order, OrderItem, RevenueReport, AdminRevenueReport, LikeMenuItem, LikeStore
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.template.response import TemplateResponse
from django.urls import path
from foods.models import Category
from django.db.models import Count


class MyAdminSite(admin.AdminSite):
    site_header = 'FoodApp'

    def get_urls(self):
        return [path('cate-stats/', self.stats)] + super().get_urls()

    def stats(self, request):
        stats = Category.objects.annotate(counter=Count('store__id')).values('id', 'name', 'counter')
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': stats
        })


admin_site = MyAdminSite(name='FoodApp')


class StoreForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Store
        fields = '__all__'


class MyStoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'location', 'created_date', 'updated_date', 'active']
    search_fields = ['id', 'name']
    list_filter = ['created_date', 'name', 'active']
    readonly_fields = ['my_image']
    form = StoreForm

    def my_image(self, food):
        if food.image:
            return mark_safe(f"<img src='/static/{food.image.name}' width='200' />")


admin_site.register(Category)
admin_site.register(Store, MyStoreAdmin)
admin_site.register(MenuItem)
admin_site.register(Tag)
admin_site.register(Comment)
admin_site.register(ReviewStore)
admin_site.register(ReviewMenuItem)
admin_site.register(Order)
admin_site.register(OrderItem)
admin_site.register(RevenueReport)
admin_site.register(LikeMenuItem)
admin_site.register(AdminRevenueReport)

# Register your models here.
