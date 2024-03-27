from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView,DeleteView, TemplateView

from products.models import Product, Category, ProductReview, CartOrder, Checkout
from accounts.models import Vendor
from .forms import CartOrderForm, CheckoutForm, ProductForm, ProductReviewForm, SubscriptionForm


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    queryset = Product.objects.all().order_by("-date_published")
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        context['top_rated'] = ProductReview.objects.filter(rating=5)
        context['vendors'] = Vendor.objects.all()
        context['self_vendor'] = Vendor.objects.filter(user=self.request.user)

        context['carts'] = CartOrder.objects.filter(user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))['price__sum']


        return context
    

class CategoryProductList(LoginRequiredMixin, ListView):
    model = Product

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Product.objects.filter(category__id=category_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')

        context['vendors'] = Vendor.objects.all()
        context['carts'] = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)
        context['categories'] = Category.objects.all()
        context['category'] = Category.objects.get(pk=category_id)
        return context
    

class ProductDetail(LoginRequiredMixin, DetailView ,FormView):
    model = Product
    template_name = 'products/product-detail.html'
    form_class = CartOrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        context['vendors'] = Vendor.objects.all()
        context['carts'] = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)

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
  

class ShopDetail(LoginRequiredMixin, DetailView):
    model = Vendor
    template_name = 'products/shop-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vendors'] = Vendor.objects.all()
        context['self_vendor'] = Vendor.objects.filter(user=self.request.user)
        context['categories'] = Category.objects.all()
        context['carts'] = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))[
            'price__sum']

        return context


class ShoppingCart(LoginRequiredMixin, TemplateView):
    template_name = 'products/shopping-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['carts'] = CartOrder.objects.filter(user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))['price__sum']
        context['vendors'] = Vendor.objects.all()
        context['self_vendor'] = Vendor.objects.filter(user=self.request.user)

        return context
    

class DeleteCartItemView(LoginRequiredMixin, DeleteView):
    model = CartOrder
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        cart_order = get_object_or_404(
            CartOrder, id=self.kwargs['pk'], user=self.request.user, checked_out=False)
        cart_order.delete()
        return redirect("index")


class CheckoutView(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'products/checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vendors'] = Vendor.objects.all()
        context['categories'] = Category.objects.all()
        context['carts'] = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))[
            'price__sum']
        return context

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']

        # Check if the entered username and password are valid
        user = authenticate(username=username, password=password)

        if user is not None:
            # Valid credentials, proceed with the checkout
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']

            # Get all CartOrder instances for the current user that haven't been checked out
            cart_orders = CartOrder.objects.filter(
                user=self.request.user, checked_out=False)

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

                cart_order.checked_out = True
                cart_order.payment_status = True
                cart_order.save()

            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)
        
    def get_success_url(self):
        return reverse_lazy('cart') 


class CreateProductView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    success_url = reverse_lazy("index")
    template_name = "products/createProduct.html"

    def form_valid(self, form):
        vendor_pk = self.kwargs.get('pk')
        vendor = get_object_or_404(Vendor, pk=vendor_pk)

        form.instance.vendor = vendor

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        context['top_rated'] = ProductReview.objects.filter(rating=5)
        context['vendors'] = Vendor.objects.all()
        context['self_vendor'] = Vendor.objects.filter(user=self.request.user)

        context['carts'] = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))[
            'price__sum']

        return context
    

class CreateReviewView(LoginRequiredMixin, CreateView):
    form_class = ProductReviewForm
    success_url = reverse_lazy("index")
    template_name = "products/createReview.html"

    def form_valid(self, form):
        product_pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)

        form.instance.product = product
        form.instance.user = self.request.user 

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        context['top_rated'] = ProductReview.objects.filter(rating=5)
        context['vendors'] = Vendor.objects.all()
        context['self_vendor'] = Vendor.objects.filter(user=self.request.user)

        context['carts'] = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))[
            'price__sum']

        return context


class SubscriptionView(LoginRequiredMixin, CreateView):
    form_class = SubscriptionForm
    success_url = reverse_lazy("create-vendor")
    template_name = "products/subscription.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.paid = True

        duration = form.cleaned_data.get('duration')

        if duration == '1':  # Monthly
            form.instance.amount = 5000
        elif duration == '2':  # Yearly
            form.instance.amount = 50000


        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        context['top_rated'] = ProductReview.objects.filter(rating=5)
        context['vendors'] = Vendor.objects.all()
        context['self_vendor'] = Vendor.objects.filter(user=self.request.user)

        context['carts'] = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)

        carts_queryset = CartOrder.objects.filter(
            user=self.request.user, checked_out=False)
        context['total_price_sum'] = carts_queryset.aggregate(Sum('price'))[
            'price__sum']

        return context
