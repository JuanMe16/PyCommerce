from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", views.StoreHomeView.as_view(), name="index"),
    path("about-us/", views.AboutView.as_view(), name="about-us"),
    path(
        "categories/<int:category_id>/", views.CategoryView.as_view(), name="category"
    ),
    path("product/<int:product_id>/", views.ProductView.as_view(), name="product"),
    path(
        "add-product/",
        login_required(views.PurchaseView.as_view(), login_url="index"),
        name="add-product",
    ),
    path(
        "delete-product/<int:checkout_product>/",
        login_required(views.DeletePurchaseView.as_view(), login_url="index"),
        name="delete-product",
    ),
    path(
        "checkout/",
        login_required(views.CheckoutView.as_view(), login_url="index"),
        name="checkout",
    ),
    path(
        "add-purchase/<int:checkout_product>/",
        login_required(views.AddPurchaseView.as_view(), login_url="index"),
        name="add-purchase",
    ),
    path(
        "reduce-purchase/<int:checkout_product>/",
        login_required(views.RemovePurchaseView.as_view(), login_url="index"),
        name="reduce-purchase",
    ),
    path(
        "save-review/<int:product_id>/",
        login_required(views.SaveReviewView.as_view(), login_url="index"),
        name="save-review",
    ),
    path(
        "charge/",
        login_required(views.ChargeView.as_view(), login_url="index"),
        name="charge",
    ),
]
