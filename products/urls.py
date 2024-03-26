from django.urls import path
from products.views import (
    ProductListView,
    CategoryProductList,
    ProductDetail,
    ShopDetail,
    ShoppingCart,
    DeleteCartItemView,
    CheckoutView,
    CreateProductView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("product/<int:pk>/detail/", ProductDetail.as_view(), name="product"),
    path("create/<int:pk>/product/", CreateProductView.as_view(), name="create-product"),

    path("cart/", ShoppingCart.as_view(), name="cart"),
    path("cart/<int:pk>/delete/", DeleteCartItemView.as_view(), name="delete-cart"),
    path("chekout/", CheckoutView.as_view(), name="checkout"),

    path("vendor/<int:pk>/detail/", ShopDetail.as_view(), name="vendor"),
    path("category/<int:pk>/products/",
         CategoryProductList.as_view(), name="category"),
]
