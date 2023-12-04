from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.StoreHomeView.as_view(), name="index"),
    path("about-us/", views.AboutView.as_view(), name="about-us"),
    path("categories/<int:category_id>", views.CategoryView.as_view(), name="category"),
    path("product/<int:product_id>", views.ProductView.as_view(), name="product"),
    path("add-product/", login_required(views.AddCartView.as_view()), name="add-product"),
    path("checkout/", login_required(views.CheckoutView.as_view()), name="checkout"),
    path("save-address/", login_required(views.SaveAddressView.as_view()), name="save-address"),
]
