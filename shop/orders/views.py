# orders/views.py
from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail

def order_create(request):
    cart = Cart(request)
    if not cart:  # Проверка на пустую корзину
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            # Формируем сообщение для компании
            message = (
                f"Новый заказ #{order.id} от клиента\n\n"
                f"Клиент: {order.first_name} {order.last_name}\n"
                f"Телефон: {order.phone_number}\n"
                f"Email: {order.email}\n"
                f"Адрес доставки:\n"
                f"  Город: {order.city}\n"
                f"  Адрес: {order.address}\n"
                f"  Почтовый индекс: {order.postal_code}\n\n"
                f"Пожалуйста, обработайте заказ."
            )
            # Отправка письма компании
            send_mail(
                subject=f'Новый заказ #{order.id}',
                message=message,
                from_email='podkov_an@mail.ru',
                recipient_list=['podkov_an@mail.ru'],
                fail_silently=False,
            )
            # Сохраняем все элементы корзины
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    size=item['size']  # Добавляем размер
                )
            # Очищаем корзину после сохранения всех элементов
            cart.clear()
            return render(request,
                          'order/created.html',
                          {'order': order,
                           'form': form})
    else:
        form = OrderCreateForm(request=request)
    return render(request,
                  'order/create.html',
                  {'cart': cart,
                   'form': form})