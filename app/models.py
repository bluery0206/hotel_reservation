from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.core import validators
from datetime import date

from .utils import room_upload_path
from uuid import uuid4

class Profile(models.Model):
    """ Profile """
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        auto_created=True,
        default=uuid4,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    image = ResizedImageField(
        size = [200, 200],
        crop = ['middle', 'center'],
        upload_to = 'profile_images',
        blank = True,
        null = True,
        default = "default.png",
    )

    def __str__(self):
        return f"Profile({self.user.get_username()})"
    
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class Amenity(models.Model):
    """ Amenities """
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        auto_created=True,
        default=uuid4,
    )
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
    @property  
    def get_fee_display(self):
        return f"₱{self.fee:,.2f}" if self.fee > 0 else "Free"

    class Meta:
        """ Metadata """
        verbose_name_plural = "Amenities" # The text you see in the django admin panel


class Room(models.Model):
    """ Room """

    class RoomTypes(models.TextChoices):
        """ Room Types"""

        STANDARD = "ST", "Standard"
        DELUXE = "DL", "Deluxe"
        SUITE = "SU", "Suite"

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        auto_created=True,
        default=uuid4,
    )
    image = ResizedImageField(
        validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'jfif', 'PNG', 'JPG'])],
        upload_to = "images/rooms/",
        blank = True,
        null = True,
        default = "default.png",
    )
    name = models.CharField(
        max_length=100,
        validators = [
            validators.RegexValidator(
                r'^[a-zA-Z0-9_.\)\(\[\]\\\|\s]{4,}$',
                message = "Allowed characters: a-z, A-Z, 0-9, '_', '.', '\', '(', ')', '[', ']' and ' '."
            )
        ],
    )
    description = models.TextField(
        validators = [
            validators.RegexValidator(
                r'^[a-zA-Z0-9_.\)\(\[\]\\\|\s]+$',
                message = "Allowed characters: a-z, A-Z, 0-9, '_', '.', '\', '(', ')', '[', ']' and ' '."
            )
        ],
        blank=True
    )
    type = models.CharField(choices=RoomTypes.choices)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="rooms")
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Room({self.type}: {self.name})"
    
    @property
    def total_amenity_fee(self):
        total = 0
        if self.amenities.all():
            for amenity in self.amenities.all():
                total += amenity.fee
        return total

    
    @property
    def price(self) -> float:
        if self.amenities.exists():
            return self.base_price + self.total_amenity_fee 
        else:
            return self.base_price
    
    @property
    def get_price_display(self):
        return f"₱{self.price:,.2f}" if self.price > 0 else "Free"
    
    @property
    def get_base_price_display(self):
        return f"₱{self.base_price:,.2f}" if self.price > 0 else "Free"

    @property
    def get_capacity_display(self) -> str:
        return f"1 to {self.capacity:,} people" if self.capacity > 1 else f"{self.capacity:,} person"


class Reservation(models.Model):
    """ Reservation """
    # Delete THIS instance of User or Room is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations") 
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        auto_created=True,
        default=uuid4,
    )

    date_checkin = models.DateField(blank=True, null=True)  # Start date
    date_checkout = models.DateField(blank=True, null=True)  # End date

    date_bookat = models.DateField(auto_now_add=True) 
    date_bookfrom = models.DateField(
        # Reservation date must be today or in the future
        validators=[validators.MinValueValidator(date.today())],
    )
    date_bookuntil = models.DateField(
        validators=[validators.MinValueValidator(date.today())],
    )
    paid_price = models.DecimalField(max_digits=10, decimal_places=2)  # Final price after discounts
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # e.g., 10.50%

    @property
    def days(self):
        return (self.date_bookuntil - self.date_bookfrom).days

    @property
    def get_days_display(self):
        return f"{self.days} day" if self.days == 1 else f"{self.days} days"