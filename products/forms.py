from django import forms
from .models import CartOrder


class CartOrderForm(forms.ModelForm):
    class Meta:
        model = CartOrder
        fields = ['quantity']
