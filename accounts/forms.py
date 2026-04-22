from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SellerProfile

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class PayoutForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['payout_method', 'account_title', 'account_number', 'iban']