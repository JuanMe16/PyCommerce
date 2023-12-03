from django.contrib import admin
from .models import Category, Product, Review, Address, Cart

# Register your models here.
admin.site.register([Category, Product, Review, Address, Cart])