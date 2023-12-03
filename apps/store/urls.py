from . import views
from django.urls import path

urlpatterns = [
    path("", views.StoreHomeView.as_view(), name="index"),
    path("about-us/", views.AboutView.as_view(), name="about-us"),
    path("categories/<int:category_id>", views.CategoryView.as_view(), name="category"),
    path("product/<int:product_id>", views.ProductView.as_view(), name="product"),
    path("add-product/", views.AddCartView.as_view(), name="add-product"),
]
