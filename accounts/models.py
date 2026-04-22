from django.db import models
from django.contrib.auth.models import User


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    PAYMENT_METHODS = (
        ('easypaisa', 'EasyPaisa'),
        ('jazzcash', 'JazzCash'),
        ('bank', 'Bank Transfer'),
    )

    payout_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)
    account_title = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    iban = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username



class WithdrawalRequest(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    account_number = models.CharField(max_length=100)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller.username} - {self.amount}"
