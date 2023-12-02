from django.contrib import admin
from .models import Category, Product, Comment

# Register your models here.
admin.site.register([Category, Product, Comment])