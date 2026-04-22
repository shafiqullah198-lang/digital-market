from django.contrib import admin
from .models import Product, Order
from accounts.models import SellerProfile


# PRODUCT ADMIN
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'rating')
    list_filter = ('category',)
    search_fields = ('title',)


# ORDER ADMIN (payment approval → add seller balance)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'approved', 'created_at')
    list_filter = ('approved',)

    def save_model(self, request, obj, form, change):

        if change:
            old = Order.objects.get(pk=obj.pk)

            # when admin approves payment
            if not old.approved and obj.approved:
                seller = obj.product.owner
                profile, _ = SellerProfile.objects.get_or_create(user=seller)

                profile.available_balance += obj.product.price
                profile.save()

        super().save_model(request, obj, form, change)
