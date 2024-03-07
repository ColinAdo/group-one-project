from django import forms
from .models import CartOrder, Checkout


class CartOrderForm(forms.ModelForm):
    class Meta:
        model = CartOrder
        fields = ['quantity']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['fname', 'lname', 'address', 'city', 'phone', 'email']
