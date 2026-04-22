from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        total = 0
        count = 0

        if cart:
            for item in cart.items.all():
                total += item.product.price * item.quantity
                count += item.quantity

        return {
            'cart': cart,
            'cart_total': total,
            'cart_count': count,
        }

    return {
        'cart': None,
        'cart_total': 0,
        'cart_count': 0,
    }
