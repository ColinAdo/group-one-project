from django.urls import path
from products.views import ProductListView, CategoryProductList

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("category/<int:pk>/products/",CategoryProductList.as_view(), name="category"),
]
