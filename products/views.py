from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import Q
from cart.models import CartItem,Cart
from .models import Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import FileResponse


def home(request):
    total_products = Product.objects.count()
    total_users = User.objects.count()

    total_paid = Product.objects.aggregate(
        total=Sum('price')
    )['total'] or 0

    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_paid': int(total_paid),
    }

    return render(request, 'home.html', context)



def product_list(request):
    products = Product.objects.all()

    # ✅ Safe user orders check
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(
            user=request.user,
            approved=True
        ).values_list('product_id', flat=True)
    else:
        user_orders = []

    # 🔍 SEARCH
    search = request.GET.get('q')
    if search:
        products = products.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    # 🧩 CATEGORY FILTER
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        products = products.filter(category__in=selected_categories)

    # 💰 PRICE FILTER
    selected_price = request.GET.get('price')
    if selected_price == '0-20':
        products = products.filter(price__lt=20)
    elif selected_price == '20-50':
        products = products.filter(price__gte=20, price__lte=50)
    elif selected_price == '50-100':
        products = products.filter(price__gte=50, price__lte=100)
    elif selected_price == '100+':
        products = products.filter(price__gte=100)

    # 📊 REAL COUNTS
    total_products = Product.objects.count()
    sellers_count = Product.objects.values('id').distinct().count()  # simple version
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': Product.CATEGORY_CHOICES,
        'selected_categories': selected_categories,
        'selected_price': selected_price,
        'total_products': total_products,
        'showing_count': products.count(),
        'sellers_count': sellers_count,
        'approved_products': list(user_orders)
    })

def sell_buy(request):
    return render(request, 'products/sell_buy.html')

def sell(request):
    if request.method == 'POST':
        Product.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            price=request.POST['price'],
            category=request.POST['category'],
            image=request.FILES.get('image'),
            project_file=request.FILES.get('project_file')
        )
        return redirect('product_list')
  # 👈 IMPORTANT
    return render(request, 'products/sell.html')
@login_required
def proceed(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return render(request, 'products/proceed.html', {
            'cart_items': [],
            'total': 0
        })

    cart_items = cart.items.all()
    total = cart.total_price()

    return render(request, 'products/proceed.html', {
        'cart_items': cart_items,
        'total': total
    })
def checkout_success(request):
    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        CartItem.objects.filter(cart=cart).delete()

    return redirect('product_list')
@login_required
def easypaisa_payment(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        return redirect('product_list')

    if request.method == "POST":
        screenshot = request.FILES.get("screenshot")

        for item in cart.items.all():
            Order.objects.create(
                user=request.user,
                product=item.product,
                payment_screenshot=screenshot,
                approved=False
            )

        # 🧹 Clear cart after creating order
        cart.items.all().delete()

        return redirect('checkout_success')

    return render(request, "products/payment.html")

@login_required
def download_project(request, pk):

    order = get_object_or_404(
        Order,
        user=request.user,
        product_id=pk,
        approved=True
    )

    product = order.product

    return FileResponse(product.project_file.open(), as_attachment=True)


