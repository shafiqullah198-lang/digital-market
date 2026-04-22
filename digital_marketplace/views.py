from products.models import Product
from django.contrib.auth.models import User
from cart.models import CartItem
from django.db.models import Sum
from django.shortcuts import render

def home(request):
    total_products = Product.objects.filter(is_active=True).count()
    total_users = User.objects.count()

    total_paid = CartItem.objects.aggregate(
    total=Sum('product__price')
)['total'] or 0


    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_paid': int(total_paid),
    }

    return render(request, 'home.html', context)
