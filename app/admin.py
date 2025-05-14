from django.contrib import admin

from . import models

admin.site.register([
    models.Profile,
    models.Amenity,
    models.Room,
    models.Reservation,
])
