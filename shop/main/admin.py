from django.contrib import admin
from .models import Product, Category, Size, ProductSize

class ProductSizeInline (admin.TabularInline):
    model = ProductSize
    extra = 4 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available'] # Параметры, которые можно изменить в любой момент
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline]

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

