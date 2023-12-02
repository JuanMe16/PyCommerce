from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('store-home')

        return super().get(request, *args, **kwargs)


class SignUpView(View):
    """
    View of Sign Up functionality, receives the form of the SignUp modal.
    """
    def post(self, request: HttpRequest):
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        cpassword = request.POST.get('cpassword', None)
        terms = request.POST.get('terms', None)

        if (cpassword != password):
            messages.warning(request, 'Contraseña invalida')
            return render(request, 'core/index.html')

        if (terms == 'on') and (username and email and password):
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            messages.success(request, 'Usuario guardado con exito! inicia sesión nuevamente.')

        return redirect('index')


class SignInView(View):
    """
    As SignUpView it takes the SignIn form and logs-in the request.
    """
    def post(self, request: HttpRequest):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if (username and password):
            auth_res = authenticate(request, username=username, password=password)
            if auth_res:
                login(request, auth_res)
                messages.success(request, 'Sesión iniciada.')
            else:
                messages.warning(request, 'Credenciales invalidas.')
        else:
            messages.warning(request, 'Digita ambos campos en las credenciales.')

        return redirect('index')


class SignOutView(View):
    """
    logs-out the request and ends the user session.
    """
    def get(self, request: HttpRequest):
        logout(request)
        messages.success(request, 'Has salido de tu cuenta.')

        return redirect('index')