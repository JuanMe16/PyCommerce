from typing import Any
from django.views import View
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import Product, Category, Cart


class BaseTemplateView(TemplateView):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["nav_categories"] = Category.objects.values()
        context["cart_products"] = 0
        if self.request.user.is_authenticated:
            context["cart_products"] = Cart.objects.filter(
                user=self.request.user
            ).count()
        context["category_name"] = "Central de ventas"
        return context


class SearchTemplateView(BaseTemplateView):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        price_order = self.request.GET.get("price_order", None)
        if price_order == "asc":
            context["products"] = Product.objects.order_by("price")
        elif price_order == "des":
            context["products"] = Product.objects.order_by("-price")
        else:
            context["products"] = Product.objects

        return context


class StoreHomeView(SearchTemplateView):
    template_name = "store/index.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["products"] = context["products"].values()
        return context


class CategoryView(SearchTemplateView):
    template_name = "store/index.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        category_id = kwargs.get("category_id", 0)
        try:
            category = Category.objects.get(id=category_id)
            context["products"] = context["products"].filter(category=category).values()
            context["category_name"] = category.name
        except:
            self.template_name = "not_found.html"
        return context


class ProductView(BaseTemplateView):
    template_name = "store/product.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get("product_id", 0)
        try:
            product = Product.objects.get(id=product_id)
            related_products = (
                Product.objects.filter(category=product.category)
                .exclude(id=product.id)
                .values()
            )
            context["product"] = product
            context["related_products"] = related_products
        except:
            self.template_name = "not_found.html"
        return context


class AboutView(BaseTemplateView):
    template_name = "about_us.html"


class CheckoutView(BaseTemplateView):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        checkout_products = Cart.objects.filter(user=user)
        products = [
            Product.objects.get(id=product["product_id"])
            for product in checkout_products.values()
        ]
        ziped_products = zip(checkout_products, products)
        zip_sum = zip(checkout_products, products)
        context["count"] = checkout_products.count()
        context["checkout_products"] = ziped_products
        context["subtotal"] = sum(
            [product_dict.quantity * product.price for product_dict, product in zip_sum]
        )
        return context


class AddCartView(View):
    def print_message(self, request):
        messages.warning(request, "No tenemos disponible esa cantidad de ese producto")

    def post(self, request: HttpRequest):
        product_id = int(request.POST.get("product_id", None))
        quantity = int(request.POST.get("quantity", None))

        if not product_id or (not quantity or quantity < 0):
            messages.warning(request, "Datos invalidos para añadir al carrito.")
            return redirect(f"/product/{product_id}")

        try:
            user = request.user
            product = Product.objects.get(id=product_id)
            existing_cart = Cart.objects.filter(user=user, product=product).first()

            if quantity > product.stock:
                self.print_message(request)
                return redirect(f"/product/{product_id}")

            if existing_cart is None:
                new_cart = Cart.objects.create(
                    user=user, product=product, quantity=quantity
                )
                new_cart.save()
                messages.success(
                    request, f"{quantity} {product.name} se añadieron a su carrito!"
                )
            else:
                if existing_cart.quantity + quantity > product.stock:
                    self.print_message(request)
                    return redirect(f"/product/{product_id}")

                existing_cart.quantity += quantity
                existing_cart.save()
        except Exception:
            messages.warning(
                request, "Un error ha ocurrido, no se pudo procesar la compra."
            )

        return redirect(f"/product/{product_id}")

class SaveAddressView(View):
    pass