from . import views
from django.urls import path

urlpatterns = [
    path("", views.StoreHomeView.as_view(), name="index"),
    path("product/<int:product_id>", views.ProductView.as_view(), name="product"),
]
