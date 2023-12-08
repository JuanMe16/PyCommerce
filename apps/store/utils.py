import stripe
from django.conf import settings


def context_builder(context, checkout_products, products):
    ziped_products = zip(checkout_products, products)
    context["count"] = checkout_products.count()
    context["subtotal"] = calc_subtotal(checkout_products, products)
    context["checkout_products"] = ziped_products
    context["key"] = settings.STRIPE_PUBLIC_KEY
    context["stripe_price"] = context["subtotal"] * 100
    payment_intent = create_payment_intent(context)
    context["client_secret"] = payment_intent.client_secret
    return context


def calc_subtotal(checkout_products, products):
    zip_sum = zip(checkout_products, products)
    return sum(
        [product_dict.quantity * product.price for product_dict, product in zip_sum]
    )


def create_payment_intent(context):
    return stripe.PaymentIntent.create(
        api_key=settings.STRIPE_SECRET_KEY,
        amount=context["stripe_price"],
        description="Django-Marketplace Cart",
        currency="usd",
    )
