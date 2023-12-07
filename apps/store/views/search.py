from django.views.generic import TemplateView
from ..models import Product, Category, Order, Review


class BaseTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_categories"] = Category.objects.values()
        context["cart_products"] = 0
        if self.request.user.is_authenticated:
            context["cart_products"] = Order.objects.filter(
                user=self.request.user,state='CA'
            ).count()
        context["category_name"] = "Central de ventas"
        return context


class AboutView(BaseTemplateView):
    template_name = "about_us.html"


class SearchTemplateView(BaseTemplateView):
    def get_context_data(self, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = context["products"].values()
        return context


class CategoryView(SearchTemplateView):
    template_name = "store/index.html"

    def get_context_data(self, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get("product_id", 0)
        try:
            product = Product.objects.get(id=product_id)
            category = Category.objects.get(id=product.category_id)
            related_products = (
                Product.objects.filter(category=product.category)
                .exclude(id=product.id)
                .values()
            )
            context["product"] = product
            context["category"] = category.name[:3].upper()
            context["reviews"] = Review.objects.filter(product=product_id)[:5]
            context["related_products"] = related_products
        except:
            self.template_name = "not_found.html"
        return context
