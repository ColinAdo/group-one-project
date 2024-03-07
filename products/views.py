from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.generic import ListView, DetailView, TemplateView

from products.models import Product, Category, ProductReview, CartOrder, Checkout
from accounts.models import Vendor
from .forms import CartOrderForm, CheckoutForm

class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all().order_by("-date_published")
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        context['top_rated'] = ProductReview.objects.filter(rating=5)
        context['vendors'] = Vendor.objects.all()
        context['carts'] = CartOrder.objects.filter(user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))['price__sum']


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
    

class ProductDetail(DetailView,FormView):
    model = Product
    template_name = 'products/product-detail.html'
    form_class = CartOrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context
    

    def form_valid(self, form):
        self.success_url = reverse_lazy('product', args=[self.kwargs['pk']])
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        quantity = form.cleaned_data['quantity']

        total_price = float(product.price) * float(quantity)

        cart_order = CartOrder.objects.create(
            user=self.request.user,
            product=product,
            quantity=quantity,
            price=total_price,
        )

        return super().form_valid(form)
    

class ShopDetail(DetailView):
    model = Vendor
    template_name = 'products/shop-detail.html'



class ShoppingCart(TemplateView):
    template_name = 'products/shopping-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = CartOrder.objects.filter(user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))['price__sum']
        return context
    

class CheckoutView(TemplateView, FormView):
    template_name = 'products/checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))[
            'price__sum']
        return context

    def form_valid(self, form):
        fname = form.cleaned_data['fname']
        lname = form.cleaned_data['lname']
        address = form.cleaned_data['address']
        city = form.cleaned_data['city']
        phone = form.cleaned_data['phone']
        email = form.cleaned_data['email']
        # password = form.cleaned_data['password']

        # Get all CartOrder instances for the current user that haven't been checked out
        cart_orders = CartOrder.objects.filter(user=self.request.user, checked_out=False)
        total_amount = cart_orders.aggregate(Sum('price'))['price__sum']
         
        
        for cart_order in cart_orders:
            Checkout.objects.create(
                user=self.request.user,
                cart=cart_order,
                fname=fname,
                lname=lname,
                address=address,
                city=city,
                phone=phone,
                email=email,
                amount=cart_order.price,
            )
            # Mark the CartOrder as checked out
            cart_order.checked_out = True
            cart_order.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('cart') 

