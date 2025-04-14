from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
# from django.utils.http import urlsafe_base64_decode

# from pathlib import Path
# from uuid import uuid4

import logging

from .forms import SignUpForm, SignInForm

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    """ Shows the index/home/dashboard page """

    context = {
    #     'form': UserRegisterForm()
    }

    return render(request, "app/index.html", context)


def signin(request: HttpRequest) -> HttpResponse:
    """ User Login View """

    form = SignInForm()
    prev = request.GET.get("prev", "")
    next = request.GET.get("next", "")

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)

        logger.debug("POST")

        if form.is_valid():
            login(request, form.get_user())
            return redirect('app-index')

    context = {
        'prev': request.GET.get("prev", ""),
        'next': request.GET.get("next", ""),
        'form': form,
    }

    return render(request, "app/signin.html", context)


def signup(request: HttpRequest) -> HttpResponse:
    """ User Register View """

    form = SignUpForm()
    prev = request.GET.get("prev", "")
    next = request.GET.get("next", "")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            msg = f"User ({form.cleaned_data.get("username")}) successfully created."
            messages.success(request, msg)
            logger.debug(msg)
            return redirect(next)

    context = {
        'prev': request.GET.get("prev", ""),
        'next': request.GET.get("next", ""),
        'form': form,
    }

    return render(request, "app/signup.html", context)


def signout(request: HttpRequest) -> HttpResponse:
    """ Logouts the user """

    next = request.GET.get("next", "")

    logout(request)

    return redirect(next if next else 'app-index')
