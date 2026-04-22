from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
from django.contrib import messages
from .forms import SignupForm
from .models import SellerProfile, WithdrawalRequest
from products.models import Product, Order
from .forms import PayoutForm

def login_view(request):
    form = AuthenticationForm(data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('/')

    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    form = SignupForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('/')

    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def dashboard(request):

    user = request.user

    # USER PROFILE (seller wallet)
    profile, _ = SellerProfile.objects.get_or_create(user=user)

    # 🔹 HANDLE payout form submit
    if request.method == "POST":
        form = PayoutForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Payout details updated")
    else:
        form = PayoutForm(instance=profile)

    # BUYER PURCHASES
    purchases = Order.objects.filter(user=user, approved=True)

    # SELLER PRODUCTS
    seller_products = Product.objects.filter(owner=user)

    # SELLER SALES
    sales = Order.objects.filter(product__owner=user, approved=True)

    # TOTAL EARNINGS
    earnings = sales.aggregate(total=Sum('product__price'))['total'] or 0

    # WITHDRAWALS
    withdrawals = WithdrawalRequest.objects.filter(seller=user).order_by('-created_at')

    return render(request, 'accounts/dashboard.html', {
        'purchases': purchases,
        'sales': sales,
        'earnings': earnings,
        'seller_products': seller_products,
        'profile': profile,
        'withdrawals': withdrawals,
        'form': form,   # 🔴 VERY IMPORTANT (send form to template)
    })

@login_required
def withdraw_request(request):

    profile = SellerProfile.objects.get(user=request.user)

    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))
        method = request.POST.get("method")
        account = request.POST.get("account")
        if not profile.payout_method or not profile.account_number:
            messages.error(request, "Please add payout details first")
            return redirect('payout_settings')
        
        if amount < 10:
            messages.error(request, "Minimum withdrawal is $10")
            return redirect("withdraw")

        if amount > Decimal(profile.available_balance):
            messages.error(request, "Insufficient balance")
            return redirect("withdraw")

        WithdrawalRequest.objects.create(
    seller=request.user,
    amount=amount,
    payment_method=profile.payout_method,
    account_number=profile.account_number
)

        profile.available_balance -= amount
        profile.pending_balance += amount
        profile.save()

        messages.success(request, "Withdrawal request submitted")
        return redirect('dashboard')


    return render(request, "products/withdraw.html", {"profile": profile})


@login_required
def payout_settings(request):

    profile, _ = SellerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PayoutForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PayoutForm(instance=profile)

    return render(request, "accounts/payout_settings.html", {"form": form})