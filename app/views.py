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

from .forms import (
    SignUpForm, 
    SignInForm, 
    ProfileUpdateForm, 
    UserUpdateForm,
    AmenityForm,
    RoomForm,
)
from .models import (
    Profile, 
    Amenity,
    Room,
    RoomImage,
)

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
            return redirect(next if next else 'app-index')

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
            msg = f"User({u_form.cleaned_data.get("username")}) successfully updated."
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


def amenity_index(request: HttpRequest) -> HttpResponse:
    """ A dummy view """

    amenities = Amenity.objects.all()

    context = {
        'amenities': amenities,
    }

    return render(request, "app/amenity/amenity.html", context)

def add_amenity(request):
    """ View for adding amenity"""

    form = AmenityForm()

    if request.method == "POST":
        form = AmenityForm(request.POST)

        if form.is_valid():
            form.save()
            msg = f"Amenity({form.instance.name}) succesfully added."
            logger.debug(msg)
            messages.success(request, msg)

    context = {
        'form': form,
        'title': "Add Amenity",
        'button_message': "Confirm",
    }

    return render(request, "app/amenity/amenity_form.html", context)

def update_amenity(request: HttpRequest, pk:int) -> HttpResponse:
    """ View for adding amenity"""

    amenity = get_object_or_404(Amenity, pk=pk)
    form = AmenityForm(instance=amenity)

    if request.method == "POST":
        form = AmenityForm(request.POST, instance=amenity)

        if form.is_valid():
            form.save()
            msg = f"Amenity({form.instance.name}) succesfully updated."
            logger.debug(msg)
            messages.success(request, msg)

    context = {
        'form': form,
        'title': f"Update Amenity({amenity.name})",
        'button_message': "Confirm changes",
    }

    return render(request, "app/amenity/amenity_form.html", context)


def delete_amenity(request: HttpRequest, pk:int) -> HttpResponse:
    """ View for adding amenity"""

    amenity = get_object_or_404(Amenity, pk=pk)

    if request.method == "POST":
        name = amenity.name
        amenity.delete()
        msg = f"Amenity({name}) succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)

    context = {
        'amenity': amenity,
        'title': f"Delete Amenity({amenity.name})",
        'description': f"Deleting Amenity({amenity.name}) can't be undone.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)


def delete_all_amenity(request: HttpRequest) -> HttpResponse:
    """ View for adding amenity"""

    if request.method == "POST":
        amenities = Amenity.objects.all()
        n_amenities = len(amenities)

        for amenity in amenities:
            amenity.delete()

        msg = f"Amenity ({n_amenities}) succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)

    context = {
        'title': "Delete all amenity",
        'description': "Deleting Amenities can't be undone.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)


def room_index(request: HttpRequest) -> HttpResponse:
    """ A dummy view """

    rooms = Room.objects.all()

    context = {
        'rooms': rooms,
    }

    return render(request, "app/room/room_index.html", context)


def add_room(request):
    """ View for adding rooms"""

    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            msg = f"{form.instance} succesfully added."
            logger.debug(msg)
            messages.success(request, msg)

    context = {
        'form': form,
        'title': "Add Room",
        'button_message': "Confirm",
    }

    return render(request, "app/room/room_form.html", context)


def update_room(request, pk):
    """ View for adding rooms"""

    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            msg = f"{form.instance} succesfully updated."
            logger.debug(msg)
            messages.success(request, msg)

    context = {
        'form': form,
        'title': "Update Room",
        'button_message': "Confirm",
    }

    return render(request, "app/room/room_form.html", context)


def delete_room(request, pk):
    """ View for adding rooms"""

    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        room.delete()
        msg = f"{room} succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)

    context = {
        'title': f"Delete Room({room.name})",
        'description': f"Deleting Room({room.name}) can't be undone.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)


def delete_all_room(request):
    """ View for adding rooms"""

    if request.method == "POST":
        rooms = Room.objects.all()
        n_rooms = len(rooms)

        for room in rooms:
            room.delete()

        msg = f"Rooms({n_rooms}) succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)

    context = {
        'title': "Delete all rooms",
        'description': "Deleting rooms can't be undone.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)

