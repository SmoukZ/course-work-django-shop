from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0  # Не добавлять пустые строки по умолчанию

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'created', 'updated', 'is_processed']
    list_filter = ['created', 'updated', 'is_processed']
    list_editable = ['is_processed']
    search_fields = ['id', 'first_name', 'last_name', 'email']
    inlines = [OrderItemInline]
    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f"{updated} заказ(ов) отмечены как обработанные.")
    mark_as_processed.short_description = "Отметить выбранные заказы как обработанные"