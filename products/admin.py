from django.contrib import admin
from django.utils.html import mark_safe

from products.models import Category, Product, ProductImages, CartOrder, Wishlist, ProductReview

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "display_image", "date"]

    def display_image(self, obj):
        return mark_safe('<a href="{}"> <img src="{}" width="30" height="30" style="border-radius: 50%;" /> </a>'.format(obj.image.url, obj.image.url))
    display_image.short_description = 'Image'


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = [
        "name",
        "vendor",
        "display_image",
        "product_type",
        "price",
        "number_in_stock"]

    def display_image(self, obj):
        return mark_safe('<a href="{}"> <img src="{}" width="30" height="30" style="border-radius: 50%;" /> </a>'.format(obj.image.url, obj.image.url))
    display_image.short_description = 'Image'


class WishlistAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product",
        "date",
    ]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product",
        "rating",
        "date",
    ]

class CartOrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product",
        "price",
        "payment_status",
        "product_status",
        "quantity",
        "order_date",
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
