from typing import Any
from django.views.generic import TemplateView
from .models import Product


class StoreHomeView(TemplateView):
    template_name = "store/index.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['products'] = [product for product in Product.objects.values()]
        return context


class ProductView(TemplateView):
    template_name = "store/product.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get('product_id', 0)
        try:
            context['product'] = Product.objects.get(id=product_id)
        except:
            self.template_name = 'not_found.html'
        return context
