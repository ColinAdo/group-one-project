from django.shortcuts import render
from django.views.generic.list import ListView

from products.models import Product
class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()
