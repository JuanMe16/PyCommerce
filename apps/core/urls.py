from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('auth/sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('auth/sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('auth/sign-out/', views.SignOutView.as_view(), name='sign-out'),
]