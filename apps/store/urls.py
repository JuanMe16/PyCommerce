from . import views
from django.urls import path

urlpatterns = [
    path('', views.StoreHomeView.as_view(), name='store-home')
]