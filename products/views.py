from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product, Category

class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
