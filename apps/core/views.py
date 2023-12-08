from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http.request import HttpRequest
from apps.core.models import User
from django.contrib.auth import authenticate, login, logout

def custom_404_error(request, _):
    return render(request, "not_found.html", status=404)


class SignUpView(View):
    """
    View of Sign Up functionality, receives the form of the SignUp modal.
    """

    def post(self, request: HttpRequest):
        firstname = request.POST.get("firstname", None)
        lastname = request.POST.get("lastname", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        cpassword = request.POST.get("cpassword", None)
        terms = request.POST.get("terms", None)
        next_url = request.GET.get("next", None)

        if cpassword != password:
            messages.warning(request, "Contraseña invalida")
            return render(request, "core/index.html")

        if (terms == "on") and (firstname and lastname and email and password):
            new_user = User.objects.create_user(email, password)
            new_user.first_name = firstname
            new_user.last_name = lastname
            new_user.save()
            messages.success(
                request, "Usuario guardado con exito! inicia sesión nuevamente."
            )

        if next_url is not None:
            return redirect(next_url)
        return redirect("index")


class SignInView(View):
    """
    As SignUpView it takes the SignIn form and logs-in the request.
    """

    def post(self, request: HttpRequest):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        next_url = request.GET.get("next", None)

        if username and password:
            auth_res = authenticate(request, username=username, password=password)
            if auth_res:
                login(request, auth_res)
                messages.success(request, "Sesión iniciada.")
            else:
                messages.warning(request, "Credenciales invalidas.")
        else:
            messages.warning(request, "Digita ambos campos en las credenciales.")

        if next_url is not None:
            return redirect(next_url)
        return redirect("index")


class SignOutView(View):
    """
    logs-out the request and ends the user session.
    """

    def get(self, request: HttpRequest):
        next_url = request.GET.get("next", None)
        logout(request)
        messages.success(request, "Has salido de tu cuenta.")

        if next_url is not None:
            return redirect(next_url)
        return redirect("index")
