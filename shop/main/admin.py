from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 
                    'available', 'created', 'updated', 'get_sizes_display']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available'] # Параметры, которые можно изменить в любой момент
    prepopulated_fields = {'slug': ('name',)}
    help_texts = {
        'sizes': 'Введите размеры через запятую (например, S,M,L). Доступные размеры: S, M, L, XL.'
    }