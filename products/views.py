from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from products.models import Product, Category, ProductReview
from accounts.models import Vendor

class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all().order_by("-date_published")
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        context['top_rated'] = ProductReview.objects.filter(rating=5)
        context['vendors'] = Vendor.objects.all()
        return context
    
class CategoryProductList(ListView):
    model = Product

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Product.objects.filter(category__id=category_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context['categories'] = Category.objects.all()
        context['category'] = Category.objects.get(pk=category_id)
        return context
    

class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context
    

class ShopDetail(DetailView):
    model = Vendor
    template_name = 'products/shop-detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = Vendor.objects.all()
    #     return context

