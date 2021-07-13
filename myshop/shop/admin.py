from django.contrib import admin
from .models import Product,Category
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'category_slug']
    prepopulated_fields = {'category_slug': ('category_name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available', 'price']
    prepopulated_fields = {'product_slug': ('product_name',)}