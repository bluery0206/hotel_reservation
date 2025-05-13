from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator

from .utils import room_upload_path


class Profile(models.Model):
    """ Profile """
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


class Amenity(models.Model):
    """ Amenities """
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        """ Metadata """
        verbose_name_plural = "Amenities" # The text you see in the django admin panel


class Room(models.Model):
    """ Room """

    class RoomTypes(models.IntegerChoices):
        """ Room Types"""

        STANDARD = 0, "Standard"
        DELUXE = 1, "Deluxe"
        SUITE = 2, "Suit"

    image = ResizedImageField(
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'jfif', 'PNG', 'JPG'])],
        upload_to = "images/rooms/",
        blank = True,
        null = True,
        default = "default.png",
    )
    name = models.CharField(
        max_length=100,
        validators = [
            RegexValidator(
                r'^[a-zA-Z0-9_.\)\(\[\]\\\|\s]{4,}$',
                message = "Allowed characters: a-z, A-Z, 0-9, '_', '.', '\', '(', ')', '[', ']' and ' '."
            )
        ],
    )
    description = models.TextField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z0-9_.\)\(\[\]\\\|\s]{4,}$',
                message = "Allowed characters: a-z, A-Z, 0-9, '_', '.', '\', '(', ')', '[', ']' and ' '."
            )
        ],
    )
    type = models.IntegerField(choices=RoomTypes.choices)
    amenities = models.ManyToManyField(Amenity, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room({self.type}: {self.name})"


class Booking(models.Model):
    """ Booking """
    # Delete THIS instance of User or Room is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    check_in = models.DateTimeField()  # Start date
    check_out = models.DateTimeField()  # End date

    booked_at = models.DateTimeField(auto_now_add=True) 
    book_until = models.DateTimeField()

    paid_price = models.DecimalField(max_digits=10, decimal_places=2)  # Final price after discounts
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # e.g., 10.50%
