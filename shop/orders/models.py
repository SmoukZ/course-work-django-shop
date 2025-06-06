from django.db import models
from main.models import Product
from users.models import User

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT,
                             blank=True, null=True, default=None)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField()
    city = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20) # Почтовый индекс
    phone_number = models.CharField(max_length=20)  # Номер телефона
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_processed = models.BooleanField(default=False, verbose_name="Обработан")  # Новое поле

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['is_processed']),  # Индекс для фильтрации
        ]

    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} (Size: {self.size or 'N/A'})"
    
    def get_cost(self):
        return self.price * self.quantity