from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST, product=product)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            size=cd['size'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')
    if not size:
        # Попробуем найти размер в корзине
        possible_keys = [key for key in cart.cart.keys() if key.startswith(f"{product_id}_")]
        if possible_keys:
            size = possible_keys[0].split('_')[1]
    cart.remove(product, size=size)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True,
                'size': item['size']
            },
            product=item['product']
        )
    return render(request, 'cart/detail.html', {'cart': cart})