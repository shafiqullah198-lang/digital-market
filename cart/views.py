from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    total = cart.total_price() if cart else 0

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'total': total
    })


@login_required
def cart_add_ajax(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return JsonResponse({
        'success': True,
        'count': sum(i.quantity for i in cart.items.all()),
        'total': cart.total_price()
    })


@login_required
def cart_update_ajax(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    action = request.GET.get('action')

    if action == 'inc':
        item.quantity += 1
        item.save()
    elif action == 'dec':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return JsonResponse({
        'success': True,
        'count': sum(i.quantity for i in item.cart.items.all()),
        'total': item.cart.total_price()
    })


@login_required
def cart_remove_ajax(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    cart = item.cart
    item.delete()

    return JsonResponse({
        'success': True,
        'count': sum(i.quantity for i in cart.items.all()),
        'total': cart.total_price()
    })
@login_required
def cart_panel(request):
    cart = Cart.objects.filter(user=request.user).first()
    total = 0
    if cart:
        total = sum(i.product.price * i.quantity for i in cart.items.all())

    return render(request, 'cart/cart_panel.html', {
        'cart': cart,
        'cart_total': total
    })
