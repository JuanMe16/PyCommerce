import stripe
from django.conf import settings


def create_customer(name, email):
    new_customer = stripe.Customer.create(
        api_key=settings.STRIPE_SECRET_KEY, name=name, email=email
    )
    return new_customer.id
