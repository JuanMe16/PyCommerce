import os
from django.db import models
from apps.core.models import User


# Create your models here.
def locate_product_img(instance, filename: str):
    return os.path.join(f"store/category_{instance.category.id}", filename)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    street = models.CharField(max_length=140)
    postal_code = models.IntegerField()
    note = models.TextField()

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return self.country + self.city + self.street


class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    discount = models.FloatField(default=0)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=95)
    photo = models.ImageField(upload_to=locate_product_img)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.IntegerField()
    discount = models.FloatField(default=0)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS = [
        ("CA", "IN CART"),
        ("PE", "PENDING"),
        ("RE", "RECEIVED"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    state = models.CharField(choices=ORDER_STATUS, default="CA")

    class Meta:
        db_table = "orders"

    def __str__(self):
        return self.user + " Order " + self.product.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    note = models.TextField()

    class Meta:
        db_table = "comments"

    def __str__(self):
        return self.note
