from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote # For decoding encoded urls (e.g. https%3A%2F%2Fexample.com -> https://example.com)
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode

# from pathlib import Path
# from uuid import uuid4

import logging

from .forms import SignUpForm, SignInForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile

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

    # Decodes URL string back into a clickable URL
    # Example:
    #   https%3A%2F%2Fexample.com -> https://example.com
    prev = unquote(prev) if prev else prev
    next = unquote(next) if next else next

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        logger.debug("User's credentials accepted. Validating...")

        if form.is_valid():
            logger.debug("User's credentials are VALID. Logging in...")
            login(request, form.get_user())
            output_msg = f"User ({form.get_user().username}) successfuly signed in."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'app-signin')

    context = {
        'prev': prev,
        'next': next,
        'form': form,
    }

    return render(request, "app/auth/signin.html", context)


def signup(request: HttpRequest) -> HttpResponse:
    """ User Register View """

    form = SignUpForm()
    prev = request.GET.get("prev", "")
    next = request.GET.get("next", "")

    # Decodes URL string back into a clickable URL
    # Example:
    #   https%3A%2F%2Fexample.com -> https://example.com
    prev = unquote(prev) if prev else prev
    next = unquote(next) if next else next

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            msg = f"User ({form.cleaned_data.get("username")}) successfully created."
            messages.success(request, msg)
            logger.debug(msg)
            return redirect(next)

    context = {
        'prev': prev,
        'next': next,
        'form': form,
    }

    return render(request, "app/auth/signup.html", context)


def signout(request: HttpRequest) -> HttpResponse:
    """ Logouts the user """
    user = request.user
    logout(request)
    output_msg = f"User ({user.username}) successfuly signed out."
    logger.debug(output_msg)
    messages.success(request, output_msg)
    return redirect('app-index')


@login_required
def profile(request: HttpRequest, pk:int) -> HttpResponse:
    """ Shows the user profile """

    p = get_object_or_404(Profile, pk=pk)
    p_form = ProfileUpdateForm(instance=p)
    u_form = UserUpdateForm(instance=p.user)

    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=p)
        u_form = UserUpdateForm(request.POST, instance=p.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            msg = f"User ({u_form.cleaned_data.get("username")}) successfully updated."
            messages.success(request, msg)
            logger.debug(msg)

    context = {
        'prev': request.GET.get("prev", ""),
        'next': request.GET.get("next", ""),
        'profile': p,
        'p_form': p_form,
        'u_form': u_form,
    }

    return render(request, "app/profile/profile.html", context)


def dummy(request: HttpRequest) -> HttpResponse:
    """ A dummy view """

    return render(request, "app/dummy.html")
