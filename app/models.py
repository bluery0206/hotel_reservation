from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

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

    # def __str__(self):
    #     return f"Amenity({self.name})"

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

    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=RoomTypes.choices)
    amenities = models.ManyToManyField(Amenity)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room({self.type}: {self.name})"


class RoomImage(models.Model):
    """ Room Images """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='image')
    image = ResizedImageField(
        upload_to = room_upload_path,
        blank = True,
        null = True,
        default = "default.png",
    )


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
