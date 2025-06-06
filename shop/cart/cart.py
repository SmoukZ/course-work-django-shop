from decimal import Decimal
from django.conf import settings
from main.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, size=None, override_quantity=False):
        product_id = str(product.id)
        # Формируем ключ, включающий размер, если он есть
        item_key = f"{product_id}_{size}" if size else product_id
        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0,
                'price': str(product.price),
                'size': size,
                'product_id': product_id  # Сохраняем product_id для __iter__
            }
        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True
    
    def remove(self, product, size=None):
        product_id = str(product.id)
        # Используем тот же ключ, что и в add
        item_key = f"{product_id}_{size}" if size else product_id
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()
    
    def __iter__(self):
        # Извлекаем product_id из каждого элемента корзины
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        # Привязываем объект product к каждому элементу корзины
        product_dict = {str(product.id): product for product in products}
        for item in cart.values():
            item['product'] = product_dict[item['product_id']]
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        try:
            del self.session[settings.CART_SESSION_ID]
            self.save()
        except KeyError:
            pass

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())