from django.conf import settings
from django.db import models

from accounts.models import Vendor
from products.choices import PRODUCT_STATUS, RATINGS


def product_driectory_path(instance, filename):
    return "Product/{0}/{1}".format(instance.name, filename)


class Category(models.Model):
    title = models.CharField(max_length=200, default="Chairs")
    image = models.ImageField(upload_to='category', default='category.png')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor')

    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to=product_driectory_path, default='product.png')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=9999999999999999, decimal_places=2, default=0.0)
    old_price = models.DecimalField(
        max_digits=9999999999999999, decimal_places=2, default=0.0)

    product_type = models.CharField(
        max_length=200, default='type', null=True, blank=True)
    number_in_stock = models.IntegerField(default=0)

    in_stock = models.BooleanField(default=False)

    date_published = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Products'

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="product-images", default="product.png")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.name


class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATINGS, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.name

# Transactions
    
class CartOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999999999999999, decimal_places=2, default=0.0)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    product_status = models.CharField(max_length=30, choices=PRODUCT_STATUS, default="processing")
    quantity = models.IntegerField()
    checked_out = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Card Orders'

    def __str__(self):
        return f"{self.user.username} cart"


class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(CartOrder, on_delete=models.DO_NOTHING, null=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    amount = models.DecimalField(max_digits=99999999, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} Checkout"
