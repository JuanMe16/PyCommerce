from django.views import View
from django.http import HttpRequest
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.conf import settings
from .search import BaseTemplateView
from ..models import Product, Order
import stripe


def delete_order_product(Order_id):
    order = Order.objects.get(id=Order_id)
    order.delete()


class CheckoutView(BaseTemplateView):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        checkout_products = Order.objects.filter(user=user, state="CA")
        if not (checkout_products.count() <= 0):
            products = [
                Product.objects.get(id=product["product_id"])
                for product in checkout_products.values()
            ]
            ziped_products = zip(checkout_products, products)
            zip_sum = zip(checkout_products, products)
            context["count"] = checkout_products.count()
            context["checkout_products"] = ziped_products
            context["subtotal"] = sum(
                [
                    product_dict.quantity * product.price
                    for product_dict, product in zip_sum
                ]
            )
            context["key"] = settings.STRIPE_PUBLIC_KEY
            context["stripe_price"] = context["subtotal"] * 100
            payment_intent = stripe.PaymentIntent.create(
                api_key=settings.STRIPE_SECRET_KEY,
                amount=context["stripe_price"],
                description="Django-Marketplace Cart",
                currency="usd",
            )
            context["client_secret"] = payment_intent.client_secret
            context["return_url"] = self.request.build_absolute_uri(reverse("charge"))
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
            existing_order = Order.objects.filter(user=user, product=product).first()

            if quantity > product.stock:
                self.print_message(request)
                return redirect(f"/product/{product_id}")

            if existing_order is None:
                new_order = Order.objects.create(
                    user=user, product=product, quantity=quantity
                )
                new_order.save()
                messages.success(
                    request, f"{quantity} {product.name} se añadieron a su carrito!"
                )
            else:
                if existing_order.quantity + quantity > product.stock:
                    self.print_message(request)
                    return redirect(f"/product/{product_id}")

                existing_order.quantity += quantity
                existing_order.save()
        except Exception:
            messages.warning(
                request, "Un error ha ocurrido, no se pudo procesar la compra."
            )

        return redirect(f"/product/{product_id}")


class PurchaseOperationsView(View):
    def operation(self) -> int:
        return None

    def get(self, request: HttpRequest, *_, **kwargs):
        order_id = kwargs.get("checkout_product", None)
        if order_id is None:
            messages.warning(
                request, "El producto no ha podido ser eliminado de su carrito."
            )

        try:
            order = Order.objects.get(id=order_id)
            product = Product.objects.get(id=order.product.id)
            order.quantity += self.operation()
            if order.quantity > product.stock:
                messages.warning(request, "No hay más de ese producto.")
            elif order.quantity == 0:
                delete_order_product(order_id)
            else:
                order.save()
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
        order_id = kwargs.get("checkout_product", None)
        if order_id is None:
            messages.warning(
                request, "El product no ha podido ser eliminado de su carrito."
            )

        delete_order_product(order_id)
        return redirect("checkout")


class ChargeView(View):
    def get(self, request: HttpRequest):
        payment_intent = request.GET.get("payment_intent", None)
        context = {}
        try:
            stripe_intent = stripe.PaymentIntent.retrieve(
                id=payment_intent, api_key=settings.STRIPE_SECRET_KEY
            )
            if stripe_intent.status == "succeeded":
                cart_orders = Order.objects.filter(user=request.user)
                cart_orders.update(state="PE")
                context["message"] = "Gracias por comprar con nosotros!"
            else:
                context["message"] = "Tu compra esta siendo procesada."
        except Exception:
            context[
                "message"
            ] = "Hubo un error en la compra, intenta de nuevo más tarde."
        return render(request, "store/paid.html", context)
