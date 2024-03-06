from django.urls import path
from products.views import (
    ProductListView,
    CategoryProductList,
    ProductDetail,
    ShopDetail,
    ShoppingCart,
    Checkout,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("product/<int:pk>/detail/", ProductDetail.as_view(), name="product"),

    path("cart/", ShoppingCart.as_view(), name="cart"),
    path("chekout/", Checkout.as_view(), name="checkout"),

    path("vendor/<int:pk>/detail/", ShopDetail.as_view(), name="vendor"),
    path("category/<int:pk>/products/",
         CategoryProductList.as_view(), name="category"),
]
