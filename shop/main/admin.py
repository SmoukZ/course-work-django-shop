from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Product, Category, Size, ProductSize

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # Уменьшаем до 1, чтобы не загромождать интерфейс

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.validate_min = True  # Требуем минимум 1 заполненную форму
        formset.min_num = 1  # Минимальное количество форм для заполнения
        return formset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline]

    def save_formset(self, request, form, formsets, change):
        super().save_formset(request, form, formsets, change)
        if not change:  # Проверяем только при добавлении нового товара
            product = form.instance
            # Проверяем, есть ли хотя бы один размер
            if not ProductSize.objects.filter(product_item=product).exists():
                raise ValidationError("Необходимо указать хотя бы один размер для товара.")

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)