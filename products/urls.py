from django.urls import path
from products.views import ProductListView, CategoryProductList, ProductDetail

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("product/<int:pk>/detail/", ProductDetail.as_view(), name="product"),
    path("category/<int:pk>/products/",CategoryProductList.as_view(), name="category"),
]
