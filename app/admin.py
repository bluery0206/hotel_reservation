from django.contrib import admin

from .models import (
    Profile,
    Booking,
    Amenity,
    Room,
)

admin.site.register([
    Profile,
    Booking,
    Amenity,
    Room,
])
