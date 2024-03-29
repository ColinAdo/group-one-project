from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Sum

from accounts.forms import CustomUserCreationForm, VendorForm

from products.models import Product, Category, CartOrder, Vendor, ProductReview

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class CreateVendorView(CreateView):
    form_class = VendorForm
    success_url = reverse_lazy("index")
    template_name = "products/createVendor.html"

    def form_valid(self, form):
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
