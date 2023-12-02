from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import TemplateView


class StoreHomeView(TemplateView):
    template_name = 'store/index.html'