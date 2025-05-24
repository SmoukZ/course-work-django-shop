from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            # Формируем сообщение для компании
            message = (
                f"Новый заказ #{order.id} от клиента\n\n"
                f"Клиент: {order.first_name} {order.last_name}\n"
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
                from_email='podkovskiy13337@mail.ru',
                recipient_list=['podkovskiy13337@mail.ru'],
                fail_silently=False,
            )
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
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