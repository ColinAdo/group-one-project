from django.urls import path
from products.views import (
    ProductListView, 
    CategoryProductList, 
    ProductDetail,
    ShopDetail,
    ShoppingCart
)

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("product/<int:pk>/detail/", ProductDetail.as_view(), name="product"),

    path("cart/", ShoppingCart.as_view(), name="cart"),

    path("vendor/<int:pk>/detail/", ShopDetail.as_view(), name="vendor"),
    path("category/<int:pk>/products/",CategoryProductList.as_view(), name="category"),
]
