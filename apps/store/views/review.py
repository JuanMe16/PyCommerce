from django.views import View
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect
from ..models import Review, Product


class SaveReviewView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        product_id = kwargs.get("product_id", 0)
        next_url = request.GET.get("next", None)
        try:
            note = request.POST.get("comment", None)
            rating = request.POST.get("rate", None)
            product = Product.objects.get(id=product_id)
            new_review = Review.objects.create(
                user=request.user, product=product, note=note, rating=rating
            )
            new_review.save()
        except Exception as err:
            print(err)
            messages.warning(request, "Su comentario fue catalogado cómo invalido.")

        if next_url is not None:
            return redirect(next_url)
        return redirect("index")
