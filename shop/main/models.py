from django.db import models
from django.urls import reverse


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True) # Уникальность - нельяз добавить 2 уникальные категории товара
    slug = models.SlugField(max_length=20, unique=True) # Слаг для генерации ссылок (пробелы -> тире, нижний регистр)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Категория' # Определение в единственном числе
        verbose_name_plural = 'Категории'
    
    def get_absolute_url(self):
        return reverse("main:catalog_by_category", 
                       args=[self.slug])
    

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.PROTECT) # Нельзя удалить категорию, пока не будут удалены все продукты
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True) # год, месяц, дата: для правильно распределения при загрузке
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True) # Дата добавления товара
    updated = models.DateTimeField(auto_now=True)

    sizes = models.ManyToManyField(Size, through='ProductSize', 
                                   related_name='product_item', blank=True)

    def get_sizes_display(self):
        """Возвращает человекочитаемый список доступных размеров."""
        return ', '.join(size.name for size in self.sizes.filter(productsize__available=True))
    
    def get_sizes_list(self):
        """Возвращает список доступных размеров."""
        return list(self.sizes.filter(productsize__available=True).values_list('name', flat=True))
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self): # Используем в карточке товара: при нажатии на карточку товара, пользователь - перенаправляется на товар
        return reverse('main:product_detail',
                       args=[self.slug])
    
class ProductSize(models.Model):
    product_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product_item', 'size')
