from django import forms
from .models import CartOrder, Checkout, Product, ProductReview, Subscription

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

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = [
            "rating",
            "review"
        ]

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            "duration"
        ]
