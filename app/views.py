from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote # For decoding encoded urls (e.g. https%3A%2F%2Fexample.com -> https://example.com)
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode
from django.utils import timezone

# from pathlib import Path
# from uuid import uuid4

import logging

from . import forms, models


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def index(request):
    """ Shows the index/home/dashboard page """

    rooms = models.Room.objects.all().order_by('-date_update')[:12]
    rooms = [[room, room.reservations.filter(date_checkout__isnull=True).order_by('date_bookfrom')] for room in rooms]

    context = {
        "rooms": rooms,
    }

    return render(request, "app/index.html", context)


def signin(request):
    """ User Login View """

    form = forms.SignInForm()

    # Decodes URL string back into a clickable URL
    # Example:
    #   https%3A%2F%2Fexample.com -> https://example.com
    prev = unquote(request.GET.get("prev", "")) 
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.SignInForm(request, data=request.POST)
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


def signup(request):
    """ User Register View """

    form = forms.SignUpForm()
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.SignUpForm(request.POST)

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



@login_required
def signout(request):
    """ Logouts the user """
    user = request.user
    logout(request)
    output_msg = f"User ({user.username}) successfuly signed out."
    logger.debug(output_msg)
    messages.success(request, output_msg)
    return redirect('app-index')



@login_required
def profile_view(request, pk):
    """ Shows the user profile """

    p = get_object_or_404(models.Profile, pk=pk)
    p_form = forms.ProfileUpdateForm(instance=p)
    u_form = forms.UserUpdateForm(instance=p.user)

    if request.method == "POST":
        p_form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=p)
        u_form = forms.UserUpdateForm(request.POST, instance=p.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            msg = f"User({u_form.cleaned_data.get("username")}) successfully updated."
            messages.success(request, msg)
            logger.debug(msg)

    context = {
        'profile': p,
        'p_form': p_form,
        'u_form': u_form,
        'current_url': request.build_absolute_uri(),
    }

    return render(request, "app/profile/view.html", context)



@login_required
def profile_delete(request, pk):
    """ Shows the user profile """

    profile = get_object_or_404(models.Profile, pk=pk)
    name = profile.user.get_full_name() if profile.user.get_full_name() else profile.user.username

    if request.method == "POST":
        profile.user.delete()
        profile.delete()
        logout(request)
        msg = f"Profile({name}) succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)
        redirect("app-index")

    context = {
        'title': f"Delete Profile: {name}",
        'description': f"Deleting Profile ({name}) can't be undone. This action also deletes your user account and so you'll have to register once again in order to sign in.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)



# AMENITY VIEWS



def amenity_index(request):
    """ A dummy view """

    amenities = models.Amenity.objects.all()

    context = {
        'amenities': amenities,
        "current_url": request.build_absolute_uri(),
    }

    return render(request, "app/amenity/index.html", context)



@login_required
def amenity_add(request):
    """ View for adding amenity"""

    form = forms.AmenityForm()
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.AmenityForm(request.POST)

        if form.is_valid():
            form.save()
            msg = f"New amenity {form.instance.name} has been succesfully added."
            logger.debug(msg)
            messages.success(request, msg)
            return redirect(next if next else "amenity:index")

    context = {
        'form': form,
        'title': "Add new amenity",
        'button_message': "Confirm",
    }

    return render(request, "app/amenity/form.html", context)



@login_required
def amenity_update(request, pk:int):
    """ View for adding amenity"""

    amenity = get_object_or_404(models.Amenity, pk=pk)
    form = forms.AmenityForm(instance=amenity)
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.AmenityForm(request.POST, instance=amenity)

        if form.is_valid():
            form.save()
            msg = f"Amenity: {form.instance.name}, was succesfully updated."
            logger.debug(msg)
            messages.success(request, msg)
            return redirect(next if next else "amenity:index")

    context = {
        'form': form,
        'title': f"Update Amenity: {amenity.name}",
        'button_message': "Confirm changes",
    }

    return render(request, "app/amenity/form.html", context)



@login_required
def amenity_delete(request, pk:int):
    """ View for adding amenity"""

    amenity = get_object_or_404(models.Amenity, pk=pk)
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        name = amenity.name
        amenity.delete()
        msg = f"Amenity: {name}, succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)
        return redirect(next if next else "amenity:index")

    context = {
        'amenity': amenity,
        'title': f"Delete Amenity: {amenity.name}",
        'description': f"Deleting Amenity: {amenity.name} can't be undone. This action will also reduce the price of the rooms associated with this amenity.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)



@login_required
def amenity_delete_all(request):
    """ View for adding amenity"""

    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        amenities = models.Amenity.objects.all()
        n_amenities = len(amenities)

        for amenity in amenities:
            amenity.delete()

        msg = f"All {n_amenities} amenities succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)
        return redirect(next if next else "amenity:index")

    context = {
        'title': "Delete all amenities",
        'description': "Deleting Amenities can't be undone. This action will also reduce the price of the rooms associated with this amenity.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)



# ROOM VIEWS



def room_index(request):
    """ View for showing all available rooms"""

    # if request.user.is_superuser:   
    #     # If the user is a superuser, show all rooms
    #     rooms = models.Room.objects.all()
    # else:
    #     # If the user is not a superuser, show only available rooms
    #     rooms = models.Room.objects.filter(is_available=True)
    
    rooms = models.Room.objects.filter()
    rooms = [[room, room.reservations.filter(date_checkout__isnull=True).order_by('date_bookfrom')] for room in rooms]
    context = {
        'rooms': rooms,
        'current_url': request.build_absolute_uri(),
    }

    return render(request, "app/room/index.html", context)



@login_required
def room_add(request):
    """ View for adding rooms"""

    form = forms.RoomForm()
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.RoomForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            msg = f"New room, {form.instance}, succesfully added."
            logger.debug(msg)
            messages.success(request, msg)
        return redirect(next if next else "room:index")

    context = {
        'form': form,
        'title': "Add Room",
        'button_message': "Confirm",
    }

    return render(request, "app/room/form.html", context)



@login_required
def room_update(request, pk):
    """ View for adding rooms"""

    room = get_object_or_404(models.Room, pk=pk)
    form = forms.RoomForm(instance=room)
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.RoomForm(request.POST, request.FILES, instance=room)

        if form.is_valid():
            form.save()
            msg = f"Room {form.instance.name} was succesfully updated."
            logger.debug(msg)
            messages.success(request, msg)
        return redirect(next if next else "room:index")

    context = {
        'form': form,
        'title': "Update Room",
        'button_message': "Confirm",
    }

    return render(request, "app/room/form.html", context)



@login_required
def room_delete(request, pk):
    """ View for adding rooms"""

    room = get_object_or_404(models.Room, pk=pk)
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        room.delete()
        msg = f"Room {room.name} was succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)
        return redirect(next if next else "room:index")

    context = {
        'title': f"Delete Room: {room.name}",
        'description': f"Deleting Room: {room.name} can't be undone. All reservations on this room will also be deleted.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)



@login_required
def room_delete_all(request):
    """ View for adding rooms"""

    next = unquote(request.GET.get("next", ""))
    rooms = models.Room.objects.all()
    n_rooms = len(rooms)

    if request.method == "POST":
        for room in rooms:
            room.delete()

        msg = f"All {n_rooms} room succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)
        return redirect(next if next else "amenity:index")

    context = {
        'title': f"Delete all {n_rooms} rooms",
        'description': "Deleting rooms can't be undone. All reservations on this room will also be deleted.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)



def room_view(request, pk):
    form = forms.ReservationForm()
    room = get_object_or_404(models.Room, pk=pk)
    reservations = room.reservations.filter(date_checkout__isnull=True).order_by('date_bookfrom')

    if request.method == "POST":
        form = forms.ReservationForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.room = room
            instance.user = request.user

            overlap = models.Reservation.objects.filter(  
                date_bookfrom__lt=form.cleaned_data['date_bookuntil'],  # Existing booking ends AFTER new check-in
                date_bookuntil__gt=form.cleaned_data['date_bookfrom'],   # Existing booking starts BEFORE new check-out
                date_checkout__isnull=True,
            ).exclude(pk=instance.pk if instance else None)

            room_overlap = overlap.filter(room=room)
            user_overlap = overlap.filter(user=request.user)

            if overlap.exists():
                if room_overlap.exists():
                    msg = f"Room {room.name} is already booked for the selected dates."
                elif user_overlap.exists():
                    msg = f"You’re already booked elsewhere for one of the selected dates."

                logger.error(msg)
                form.add_error(None, msg)
            else:
                date_bookfrom, date_bookuntil = form.cleaned_data['date_bookfrom'], form.cleaned_data['date_bookuntil']
                okay = True
                if date_bookfrom == date_bookuntil:
                    msg = f"Book from and Book until should not be in the same day."
                    logger.error(msg)
                    form.add_error(None, msg)
                    okay = False
                if date_bookfrom > date_bookuntil:
                    msg = f"Book until has to be in the future, not in the past."
                    logger.error(msg)
                    form.add_error('date_bookuntil', msg)
                    okay = False

                if okay:
                    days = (date_bookuntil - date_bookfrom).days
                    paid_price = room.price * days

                    instance.paid_price = paid_price
                    instance.save()
                    msg = f"room:Reservation for room {instance.room.name} succesfully added."
                    logger.debug(msg)
                    messages.success(request, msg)
                    return redirect("room:reservation:view", instance.pk)

    context = {
        'form': form,
        'title': room.name,
        'button_message': "Confirm",
        'room': room,
        'reservations': reservations,
        'current_url': request.build_absolute_uri(),
    }

    return render(request, "app/room/room.html", context)



# RESERVATION VIEWS



def reservation_index(request):
    """ View for showing all available rooms"""

    context = {
        'title': "Resevations",
        'reservations': models.Reservation.objects.filter(user=request.user),
    }

    return render(request, "app/reservation/index.html", context)



@login_required
def reservation_delete(request, pk):
    """ View for adding rooms"""

    prev = unquote(request.GET.get('prev', ""))
    next = unquote(request.GET.get('next', ""))

    reservation = get_object_or_404(models.Reservation, pk=pk)

    if request.method == "POST":
        reservation.delete()
        msg = f"{reservation} succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)
        return redirect(next if next else 'room:reservation:index')

    context = {
        'title': f"Delete reservation({reservation.room.name})",
        'description': f"Deleting reservation({reservation.room.name}) can't be undone.",
        'button_message': "Confirm delete",
        'current_url': request.build_absolute_uri(),
    }

    return render(request, "app/base/base_dialog.html", context)



@login_required
def reservation_checkin(request, pk):
    """ View for adding rooms"""

    reservation = get_object_or_404(models.Reservation, pk=pk)
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        reservation.date_checkin = timezone.now()
        reservation.room.is_available = False
        reservation.room.save()
        reservation.save()
        msg = f"{reservation.room.name} succesfully checked in."
        logger.debug(msg)
        messages.success(request, msg)
        return redirect(next if next else "room:reservation:index")

    context = {
        'title': f"Check-in in room \"{reservation.room.name}\"",
        'description': "Once you check in, you cannot undo it.",
        'button_message': "Confirm",
    }

    return render(request, "app/base/base_dialog.html", context)



@login_required
def reservation_checkout(request, pk):
    """ View for adding rooms"""

    reservation = get_object_or_404(models.Reservation, pk=pk)
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        reservation.date_checkout = timezone.now()
        reservation.room.is_available = True
        reservation.room.save()
        reservation.save()
        msg = f"{reservation.room.name} succesfully checked out."
        logger.debug(msg)
        messages.success(request, msg)
        return redirect(next if next else "room:reservation:index", request.user.pk)

    context = {
        'title': f"Check-out in room \"{reservation.room.name}\"",
        'description': "Once you check out, you cannot undo it.",
        'button_message': "Confirm",
    }

    return render(request, "app/base/base_dialog.html", context)



@login_required
def reservation_delete_all(request):
    """ View for adding rooms"""

    if request.method == "POST":
        reservations = models.Reservation.objects.filter(user=request.user)
        n_reservations = len(reservations)

        for reservation in reservations:
            reservation.delete()

        msg = f"room:Reservations({n_reservations}) succesfully deleted."
        logger.debug(msg)
        messages.success(request, msg)
        return redirect("room:reservation:index")

    context = {
        'title': "Delete all reservations",
        'description': "Deleting reservations can't be undone.",
        'button_message': "Confirm delete",
    }

    return render(request, "app/base/base_dialog.html", context)



def reservation_view(request, pk):
    """ View for adding rooms"""
    reservation = get_object_or_404(models.Reservation, pk=pk)
    room = reservation.room

    context = {
        'title': room.name,
        'reservation': reservation,
        'room': room,
        "current_url": request.build_absolute_uri(),
    }

    return render(request, "app/room/room.html", context)


