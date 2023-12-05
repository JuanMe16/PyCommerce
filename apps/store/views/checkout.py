from django.views import View
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect
from .search import BaseTemplateView
from ..models import Product, Cart


def delete_cart_product(cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()


class CheckoutView(BaseTemplateView):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
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


class PurchaseView(View):
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


class PurchaseOperationsView(View):
    def operation(self) -> int:
        return None

    def get(self, request: HttpRequest, *_, **kwargs):
        cart_id = kwargs.get("checkout_product", None)
        print(cart_id)
        if cart_id is None:
            messages.warning(
                request, "El producto no ha podido ser eliminado de su carrito."
            )

        try:
            cart = Cart.objects.get(id=cart_id)
            product = Product.objects.get(id=cart.product.id)
            cart.quantity += self.operation()
            if cart.quantity > product.stock:
                messages.warning(request, "No hay más de ese producto.")
            elif cart.quantity == 0:
                delete_cart_product(cart_id)
            else:
                cart.save()
        except Exception as err:
            print(err)
            messages.warning(request, "Este producto no esta en su carro.")
        finally:
            return redirect("checkout")


class AddPurchaseView(PurchaseOperationsView):
    def operation(self) -> int:
        return 1


class RemovePurchaseView(PurchaseOperationsView):
    def operation(self) -> int:
        return -1


class DeletePurchaseView(View):
    def get(self, request: HttpRequest, *_, **kwargs):
        cart_id = kwargs.get("checkout_product", None)
        if cart_id is None:
            messages.warning(
                request, "El product no ha podido ser eliminado de su carrito."
            )

        delete_cart_product(cart_id)
        return redirect("checkout")
