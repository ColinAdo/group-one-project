from django import forms
from .models import CartOrder, Checkout, Product


class CartOrderForm(forms.ModelForm):
    class Meta:
        model = CartOrder
        fields = ['quantity']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['fname', 'lname', 'address', 'city', 'phone', 'email']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'image',    
            'category', 
            'name',
            'description',
            'price',
            'product_type',
            'number_in_stock',
            'in_stock',

        ]
