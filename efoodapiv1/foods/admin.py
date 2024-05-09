from django.contrib import admin
from django.utils.html import mark_safe
from foods.models import Store, Category, MenuItem, Tag, ReviewStore, ReviewMenuItem
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class StoreForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Store
        fields = '__all__'


class MyStoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'created_date', 'updated_date', 'active']
    search_fields = ['id', 'name']
    list_filter = ['created_date', 'name', 'active']
    readonly_fields = ['my_image']
    form = StoreForm

    def my_image(self, food):
        if food.image:
            return mark_safe(f"<img src='/static/{food.image.name}' width='200' />")


admin.site.register(Category)
admin.site.register(Store, MyStoreAdmin)
admin.site.register(MenuItem)
admin.site.register(Tag)
admin.site.register(ReviewStore)
admin.site.register(ReviewMenuItem)

# Register your models here.
