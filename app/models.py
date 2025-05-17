from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.core import validators
from datetime import date

from uuid import uuid4



class Profile(models.Model):
    """ Profile """

    uuid = models.UUIDField(primary_key=True, editable=False, auto_created=True, default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",)
    image = ResizedImageField(
        validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'jfif', 'PNG', 'JPG'])],
        size = [200, 200],
        crop = ['middle', 'center'],
        upload_to = 'images/profiles',
        blank = True,
        null = True,
        default = "default.png",
    )

    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        name = self.user.get_full_name() if self.user.get_full_name() else self.user.username
        return f"{self.__class__.__name__}({name=}, {self.date_add}, {self.date_update})"

    def __str__(self) -> str:
        return self.user.get_full_name() if self.user.get_full_name() else self.user.username



class Amenity(models.Model):
    """ The extras provided by the hotel """

    class Meta:
        verbose_name_plural = "Amenities" # The text you see in the django admin panel

    uuid = models.UUIDField(primary_key=True, editable=False, auto_created=True, default=uuid4)
    name = models.CharField(max_length=100,
        validators = [
            validators.RegexValidator(r'^[a-zA-Z0-9_.\s-]{2,}$',
            message = 'Allowed characters: letters, numbers, and these " _.-".'
        )]
    )
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    
    @property  
    def get_fee_display(self) -> str:
        """ The displayed format of the fee """
        return f"₱{self.fee:,.2f}" if self.fee > 0 else "Free"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name=}, {self.fee=}, {self.date_add=}, {self.date_update=})"

    def __str__(self) -> str:
        return self.name



class Room(models.Model):
    class RoomTypes(models.TextChoices):
        STANDARD = "ST", "Standard"
        DELUXE = "DL", "Deluxe"
        SUITE = "SU", "Suite"

    uuid = models.UUIDField(primary_key=True, editable=False, auto_created=True, default=uuid4)
    image = ResizedImageField(
        validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'jfif', 'PNG', 'JPG'])],
        upload_to = "images/rooms/",
        blank = True,
        null = True,
        default = "default.png",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(choices=RoomTypes.choices)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="rooms")
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    
    @property
    def total_amenity_fee(self) -> float:
        """ The total fee of all the amenities """
        total = 0
        # Adds all amenity fees is there are any
        if self.amenities.all():
            for amenity in self.amenities.all():
                total += amenity.fee
        return total

    @property
    def price(self) -> float:
        """ The total price of the room, including the base price and the total amenity fee """
        if self.amenities.exists():
            return self.base_price + self.total_amenity_fee 
        else:
            return self.base_price
    
    @property
    def get_price_display(self) -> str:
        """ The displayed format of the price """ 
        return f"₱{self.price:,.2f}" if self.price > 0 else "Free"
    
    @property
    def get_base_price_display(self):
        """ The displayed format of the base price """
        return f"₱{self.base_price:,.2f}" if self.price > 0 else "Free"

    @property
    def get_capacity_display(self) -> str:
        """ The displayed format of the capacity """
        return f"1 to {self.capacity:,} people" if self.capacity > 1 else f"{self.capacity:,} person"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name=}, {self.type=}, {self.base_price=}, {self.capacity=}, {self.date_add=}, {self.date_update=})"

    def __str__(self) -> str:
        return self.name



class Reservation(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, auto_created=True, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations") 
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")

    # Checkin and out is when the customer arrives and leaves the hotel
    date_checkin = models.DateField(blank=True, null=True)  # Start date
    date_checkout = models.DateField(blank=True, null=True)  # End date

    date_bookat = models.DateField(auto_now_add=True) # The date the user issued a reservation
    date_bookfrom = models.DateField( # The date the room is reserved
        validators=[validators.MinValueValidator(date.today())],
    )
    date_bookuntil = models.DateField( # The date of the room reservation ends
        validators=[validators.MinValueValidator(date.today())],
    )
    paid_price = models.DecimalField(max_digits=10, decimal_places=2)  # The total price paid by the user

    @property
    def days(self):
        """ The number of days the room is reserved for """
        return (self.date_bookuntil - self.date_bookfrom).days

    @property
    def get_days_display(self):
        """ The displayed format of the number of days """
        return f"{self.days} day" if self.days == 1 else f"{self.days} days"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.room.name=}, {self.user.username=}, {self.date_bookfrom=}, {self.date_bookuntil=}, {self.paid_price=})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.room.name=}"
