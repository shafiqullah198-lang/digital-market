from django.contrib import admin
from .models import SellerProfile, WithdrawalRequest


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'available_balance', 'pending_balance')

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('seller', 'amount', 'status', 'created_at')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):

        if change:
            old = WithdrawalRequest.objects.get(pk=obj.pk)

            # save status change FIRST
            super().save_model(request, obj, form, change)

            # 🔥 AFTER status becomes approved
            if old.status != "approved" and obj.status == "approved":
                profile = SellerProfile.objects.get(user=obj.seller)

                # safety
                if profile.pending_balance >= obj.amount:
                    profile.pending_balance -= obj.amount
                    profile.save()

            return

        super().save_model(request, obj, form, change)
